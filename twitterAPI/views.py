from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache

from . import twitterLogin as loginData
import tweepy
import locale

# Parameters
TWEETS_PER_PAGE = 30
TWEET_AMOUNT = 200
CACHE_DURATION = 300


# Custom functions

def api_authentication():
    auth = tweepy.OAuthHandler(
        loginData.consumer_key, loginData.consumer_secret)
    auth.set_access_token(loginData.access_token,
                          loginData.access_token_secret)
    api = tweepy.API(auth)
    return api


def validate_user(username):
    try:
        api = api_authentication()
        api.get_user(username)
        return True
    except tweepy.error.TweepError:
        return False


def get_username(request):
    if "username" in request.session:
        return request.session["username"]
    return None


def set_username(request, username):
    request.session["username"] = username.lower()


def replace_invalid_characters(username):
    return username.replace("@", "")


def get_user_data(username, request, refresh=False):
    api = api_authentication()
    user = api.get_user(username)

    username = replace_invalid_characters(username)

    try:
        profile_banner_url = user.profile_banner_url
        profile_avatar_url = user.profile_image_url.replace("_normal", "")
    except AttributeError:
        profile_banner_url = "https://images.hdqwalls.com/download/abstract-minimal-blur-5k-jj-2560x1440.jpg"
        profile_avatar_url = "https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png"

    locale.setlocale(locale.LC_ALL, '')

    cached_data = get_cached_timeline(username)

    if(cached_data == None or refresh == True):
        user_timeline = [tweet for tweet in tweepy.Cursor(
            api.user_timeline, screen_name=username, tweet_mode="extended").items(TWEET_AMOUNT)]
        cache_timeline(username, user_timeline)
    else:
        user_timeline = cached_data

    paginator = Paginator(user_timeline, TWEETS_PER_PAGE)
    page = request.GET.get("page", 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    user_data = {"username": username,
                 "display_name": user.name,
                 "description": user.description,
                 "profile_banner_url": profile_banner_url,
                 "profile_avatar_url": profile_avatar_url,
                 "follower_count": f'{user.followers_count:n}',
                 "follow_count": f'{user.friends_count:n}',
                 "user_timeline": posts,
                 }
    return user_data


def cache_timeline(username, user_timeline):
    cache.set(username, user_timeline, CACHE_DURATION)


def get_cached_timeline(username):
    return cache.get(username)


# Views

def home(request):
    return render(request, "twitterAPI/home.html")


def set_user(request):
    username = request.POST.get("twitterHandle")

    if validate_user(username):
        set_username(request, username)
        response = HttpResponseRedirect("profile")
    else:
        response = HttpResponseRedirect("/")

    return response


def profile(request):

    username = get_username(request)

    if(username is None):
        return HttpResponseRedirect("/")

    if(request.POST.get("refresh") == "refresh"):
        get_user_data(username, request, True)
        return HttpResponseRedirect('profile')
    else:
        return render(request, "twitterAPI/profile.html", get_user_data(username, request))
