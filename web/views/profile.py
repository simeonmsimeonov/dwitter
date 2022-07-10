from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from web.forms import ProfileEditForm
from web.models import Profile, Dweet, User
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def profile_list(request):
    profiles = Profile.objects.all()
    p = Paginator(profiles, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "statter/profile_list.html", {"profiles": profiles, "page_obj": page_obj})

def profile(request, pk):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(pk=pk)
    states = Dweet.objects.filter(user__id=profile.id).order_by("-created_at")
    first_followers = Profile.objects.filter(user__profile__in=profile.followed_by.all()[:3])
    followers_left = Profile.objects.filter(user__profile__in=profile.followed_by.all()[3:])
    p = Paginator(states, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")

        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(
        request, "statter/profile.html", 
        {"profile": profile, 
        "page_obj": page_obj, 
        "first_followers": first_followers, 
        "followers_left": followers_left, 
        "states": states, 
        "user": user}
    )



class ProfileEditView(views.UpdateView, auth_mixins.PermissionRequiredMixin):
    model = User
    template_name = 'statter/profile_edit.html'
    form_class = ProfileEditForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_object = list(User.objects.filter(pk=self.kwargs['pk']))
        context['profile'] = profile_object[0]
        return context
    
    def dispatch(self, request, pk):
        current_user = User.objects.filter(pk=pk)
        if not request.user.is_authenticated:
            return redirect('login')
        elif not current_user[0].id == self.request.user.id:
            return redirect('dashboard')
        
    def get_success_url(self):
        profile = self.get_object()
        return reverse_lazy('profile', kwargs={'pk': profile.pk})


class DeleteProfileView(views.DeleteView):
    model = User
    success_url = reverse_lazy("dashboard")
    template_name = "statter/user_confirm_delete.html"

    def dispatch(self, request, pk, *args, **kwargs):
        current_user = User.objects.filter(pk=pk)
        if not request.user.is_authenticated:
            return redirect('login')
        elif not current_user[0].id == self.request.user.id:
            return redirect('dashboard')
       
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_object = list(User.objects.filter(pk=self.kwargs['pk']))
        context['profile'] = profile_object[0]
        return context
    
