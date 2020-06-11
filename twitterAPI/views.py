from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import twitterLogin as loginData
import tweepy
import locale

# Custom functions


def apiLogin():
    auth = tweepy.OAuthHandler(
        loginData.consumer_key, loginData.consumer_secret)
    auth.set_access_token(loginData.access_token,
                          loginData.access_token_secret)
    api = tweepy.API(auth)
    return api


def validateUser(username):
    try:
        api = apiLogin()
        api.get_user(username)
        return True
    except tweepy.error.TweepError:
        return False


def getUsername(request):
    if "username" in request.session:
        return request.session["username"]
    return None


def setUser(request, username):
    request.session["username"] = username.lower()


def replaceInvalidCharacters(username):
    return username.replace("@", "")


def getUserData(username):
    api = apiLogin()
    user = api.get_user(username)

    username = replaceInvalidCharacters(username)

    try:
        profile_banner_url = user.profile_banner_url
        profile_avatar_url = user.profile_image_url.replace("_normal", "")
    except AttributeError:
        profile_banner_url = "https://images.hdqwalls.com/download/abstract-minimal-blur-5k-jj-2560x1440.jpg"
        profile_avatar_url = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"

    locale.setlocale(locale.LC_ALL, '')

    user_data = {"username": username,
                 "display_name": user.name,
                 "description": user.description,
                 "profile_banner_url": profile_banner_url,
                 "profile_avatar_url": profile_avatar_url,
                 "follower_count": f'{user.followers_count:n}',
                 "follow_count": f'{user.friends_count:n}',
                 "user_timeline": api.user_timeline(username, count=200),
                 }
    return user_data


# Views


def home(request):
    return render(request, "twitterAPI/home.html")


def set_user(request):
    username = request.POST.get("twitterHandle")

    if validateUser(username):
        setUser(request, username)
        response = HttpResponseRedirect("profile")
    else:
        response = HttpResponseRedirect("/")

    return response


def profile(request):
    username = getUsername(request)

    if(username is None):
        return HttpResponseRedirect("/")

    user_data = getUserData(username)
    return render(request, "twitterAPI/profile.html", user_data)
