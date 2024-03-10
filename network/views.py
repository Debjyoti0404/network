from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import *
from .forms import *

@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        target_post = Posts.objects.get(id=post_id)
        if target_post.username != request.user:
            return JsonResponse({"msg": "you are not authorized to edit this post"}, status=403)
        form_content = json.loads(request.body)
        content = form_content.get('post_content')
        target_post.post_content = content
        target_post.save()
        return JsonResponse({"msg": "operation successful"}, status=200)
    
    if request.method == "GET":
        target_post = Posts.objects.get(id=post_id)
        return JsonResponse({"content": target_post.post_content}, status=200)


@login_required
def following_posts(request):
    following_accounts = request.user.following_list.all()
    all_posts = []
    for account in following_accounts:
        for post in Posts.objects.filter(username=account):
            all_posts.append(post)
            
    paginator = Paginator(all_posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "post_form": "following_pg",
        "all_posts": page_obj,
        "all_comments": Comments.objects.all()
    })


@login_required
def follow_request(request, name):
    user_to_follow = User.objects.get(username=name)
    user_goingto_follow = User.objects.get(username=request.user.username)
    #check whether the current user already follows the visited profile
    if user_goingto_follow in user_to_follow.follower_list.all():
        user_to_follow.follower_list.remove(user_goingto_follow)
        user_to_follow.follower_count = F("follower_count") - 1
        user_to_follow.save()
        user_to_follow.refresh_from_db()
        user_goingto_follow.following_list.remove(user_to_follow)
        user_goingto_follow.following_count = F("following_count") - 1
        user_goingto_follow.save()
        user_goingto_follow.refresh_from_db()
    else:
        user_to_follow.follower_list.add(user_goingto_follow)
        user_to_follow.follower_count = F("follower_count") + 1
        user_to_follow.save()
        user_goingto_follow.save()
        user_goingto_follow.following_list.add(user_to_follow)
        user_goingto_follow.following_count = F("following_count") + 1
        user_goingto_follow.save()
        user_goingto_follow.refresh_from_db()

    return redirect('profile', name)

def index(request):
    posts = Posts.objects.all().order_by('-creation_time')
    paginator = Paginator(posts, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "post_form": PostForm(),
        "all_posts": page_obj,
        "all_comments": Comments.objects.all()
    })

@login_required
def like_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({"msg": "request method not allowed"}, status=403)
    target_post = Posts.objects.get(id=post_id)
    if request.user in target_post.liked_by.all():
        target_post.liked_by.remove(request.user)
        target_post.likes = F("likes") - 1
        target_post.save()
        target_post.refresh_from_db()
        return JsonResponse({
            "btn_status": "like",
            "like_count": target_post.likes
            }, status=200)
    else:
        target_post.liked_by.add(request.user)
        target_post.likes = F("likes") + 1
        target_post.save()
        target_post.refresh_from_db()
        return JsonResponse({
            "btn_status": "remove like",
            "like_count": target_post.likes
            }, status=200)
    

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


@login_required
def postcomment(request, post_id):
    if request.method == "POST":
        targetted_post = Posts.objects.get(id=post_id)
        form_content = json.loads(request.body)
        content = form_content.get('comment_content')
        author = User.objects.get(username=request.user.username)
        new_comment = Comments.objects.create(username=author, related_post=targetted_post, content=content)
        new_comment.save()
        return JsonResponse({"message": "Comment saved successfully."}, status=201)
 

def getcomment(request, post_id):
    if request.method == "GET":
        targetted_post = Posts.objects.get(id=post_id)
        all_comments = Comments.objects.filter(related_post=targetted_post)
        return JsonResponse([comment.serialize() for comment in all_comments], safe=False)


def profile_view(request, name):
    all_posts = User.objects.get(username=name).all_posts.all().order_by('-creation_time')
    paginator = Paginator(all_posts, 2)
    pg_number = request.GET.get("page")
    pg_obj = paginator.get_page(pg_number)
    return render(request, "network/index.html", {
        "post_form": "profile_pg",
        "user_profile": User.objects.get(username=name),
        "all_posts": pg_obj
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
