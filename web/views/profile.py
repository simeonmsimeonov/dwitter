from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from web.forms import ProfileEditForm
from web.models import Profile, Dweet, User
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    states = Dweet.objects.filter(user__id=profile.user.id).order_by("-created_at")
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
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")

        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile, "page_obj": page_obj, "first_followers": first_followers, "followers_left": followers_left, 
    "states": states})


class ProfileEditView(views.UpdateView, auth_mixins.PermissionRequiredMixin):
    model = User
    template_name = 'dwitter/profile_edit.html'
    form_class = ProfileEditForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_object = list(User.objects.filter(pk=self.kwargs['pk']))
        context['profile'] = profile_object[0]
        return context
    
    # def dispatch(self, request, pk, *args, **kwargs):
    #     current_user = User.objects.filter(pk=pk)
    #     if not request.user.is_authenticated:
    #         return redirect('login')
    #     elif not current_user[0].id == self.request.user.id:
    #         return redirect('dashboard')
        
    def get_success_url(self):
        profile = self.get_object()
        return reverse_lazy('profile', kwargs={'pk': profile.pk})


class DeleteProfileView(views.DeleteView):
    model = User
    success_url = reverse_lazy("dashboard")
    template_name = "dwitter/user_confirm_delete.html"

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
    
