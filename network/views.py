from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *

@login_required
def follow_request(request, name):
    user_to_follow = User.objects.get(username=name)
    user_goingto_follow = User.objects.get(username=request.user.username)
    if user_goingto_follow in user_to_follow.follower_list.all():
        user_to_follow.follower_list.remove(user_goingto_follow)
        user_to_follow.follower_count -= 1
        user_to_follow.save()
        user_goingto_follow.following_list.remove(user_to_follow)
        user_goingto_follow.following_count -= 1
        user_goingto_follow.save()
    else:
        user_to_follow.follower_list.add(user_goingto_follow)
        user_to_follow.follower_count += 1
        user_to_follow.save()
        user_goingto_follow.following_list.add(user_to_follow)
        user_goingto_follow.following_count += 1
        user_goingto_follow.save()

    return redirect('profile', name)

def index(request):
    post_form = PostForm()
    all_posts = Posts.objects.all()
    return render(request, "network/index.html", {
        "post_form": post_form,
        "all_posts": all_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def new_post(request):
    if request.method == "POST":
        form_content = PostForm(request.POST)
        if form_content.is_valid():
            author = User.objects.get(username=request.user.username)
            post_content = form_content.cleaned_data['post_content']

            post_obj = Posts.objects.create(username=author, post_content=post_content)
            post_obj.save()

    return redirect('index')

def profile_view(request, name):
    return render(request, "network/profile.html", {
        "user_profile": User.objects.get(username=name),
        "all_posts": User.objects.get(username=name).all_posts.all()
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
