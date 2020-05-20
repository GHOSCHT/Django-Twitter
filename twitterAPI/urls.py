from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("set_user/<str:urlUsername>", views.set_user, name="set_user"),
    path("profile", views.profile, name="profile"),
    path("followers", views.followers, name="followers"),
    path("follows", views.follows, name="follows")
]
