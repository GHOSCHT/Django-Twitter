from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("set_user", views.set_user, name="set_user"),
    path("profile", views.profile, name="profile"),
]
