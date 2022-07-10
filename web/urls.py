from django.urls import path
from web.views.authentication import SignUpView, UserLoginView, UserLogoutView
from web.views.main import SearchView, dashboard
from web.views.profile import DeleteProfileView, ProfileEditView, profile, profile_list
from web.views.state import DweetDeleteView


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("login", UserLoginView.as_view(), name="login"),
    path("logout", UserLogoutView.as_view(), name="logout"),
    path("profile/edit/<int:pk>", ProfileEditView.as_view(), name="profile edit"),
    path("profile/delete/<int:pk>", DeleteProfileView.as_view(), name="profile delete"),
    path("dweet/delete/<int:pk>", DweetDeleteView.as_view(), name="dweet delete"),
    path("search", SearchView.as_view(), name="search bar")
]
