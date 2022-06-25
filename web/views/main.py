from django.shortcuts import redirect, render
from web.forms import DweetForm
from web.models import Profile, Dweet, User
from django.views import generic as views
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def dashboard(request):
    form = DweetForm(request.POST or None)

    if not request.user.is_authenticated:
        return redirect("login")
    

    if request.method == "POST":
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dashboard")
    
    followed_dweets = Dweet.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by("-created_at")
    p = Paginator(followed_dweets, 5)
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    return render(request, "dwitter/dashboard.html", {"form": form, "dweets": followed_dweets, "page_obj": page_obj})

def profile_list(request):
    profiles = Profile.objects.all()
    
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


class SearchView(views.ListView):
    model = User
    template_name = "dwitter/search.html"


    def get_queryset(self):
        query = self.request.GET.get("q")
        objects_list = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(bio__icontains=query)
            )
        return objects_list
    
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        query = self.request.GET.get("q")
        context["q"] = query

        return context