from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from . import models

from . import twitterLogin as loginData
import tweepy
import datetime

# Custom function


def apiLogin():
    auth = tweepy.OAuthHandler(
        loginData.consumer_key, loginData.consumer_secret)
    auth.set_access_token(loginData.access_token,
                          loginData.access_token_secret)
    api = tweepy.API(auth)
    return api

# Views


def home(request):
    return render(request, "twitterAPI/home.html")


def set_user(request):
    try:
        username = request.POST.get("username")

        response = HttpResponseRedirect("profile")
        response.set_cookie("twitter_username", username)

    except:
        response = render(request, "error.html")

    return response


def profile(request):
    try:
        username = request.COOKIES.get('twitter_username')
    except:
        username = "N/A"
    return render(request, "twitterAPI/profile.html", {"username": username})


def followers(request):
    return render(request, "twitterAPI/followers.html")


def follows(request):
    return render(request, "twitterAPI/follows.html")
