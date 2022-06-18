from django.urls import path

from web.views import dashboard, profile, profile_list


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile")
]
