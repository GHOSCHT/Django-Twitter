from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from twitterAPI.models import TwitterUser

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


def getUser(username):
    api = apiLogin()
    user = api.get_user(username)

    if username[0] == "@":
        username = username.replace("@", "")

    try:
        profile_banner_url = user.profile_banner_url
        profile_avatar_url = user.profile_image_url.replace("_normal", "")
    except:
        profile_banner_url = "https://images.hdqwalls.com/download/abstract-minimal-blur-5k-jj-2560x1440.jpg"
        profile_avatar_url = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"

    user_data = {"username": username,
                 "display_name": user.name,
                 "description": user.description,
                 "profile_banner_url": profile_banner_url,
                 "profile_avatar_url": profile_avatar_url,
                 "follower_count": user.followers_count,
                 "follow_count": user.friends_count,
                 "user_timeline": api.user_timeline(username, count=100),
                 }
    return user_data

# Views


def home(request):
    searched_users = TwitterUser.objects.all().order_by("-search_date")[:9]

    return render(request, "twitterAPI/home.html", {"searched_users": searched_users})


def set_user(request):
    try:
        username = request.POST.get("twitterHandle")
        response = HttpResponseRedirect("profile")
        response.set_cookie("twitter_username", username)

        try:
            apiLogin().get_user(username)
            TwitterUser.objects.create(username=username)
        except:
            response = HttpResponseRedirect("/")

    except:
        response = render(request, "error.html")

    return response


def profile(request):
    username = request.COOKIES.get('twitter_username').lower()
    user_data = getUser(username)
    return render(request, "twitterAPI/profile.html", user_data)


def followers(request):
    return render(request, "twitterAPI/followers.html")


def follows(request):
    return render(request, "twitterAPI/follows.html")
