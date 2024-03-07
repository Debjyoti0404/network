
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("profile/<str:name>", views.profile_view, name="profile"),
    path("followrequest/<str:name>", views.follow_request, name="followrequest"),
    path("postcomment/<int:post_id>", views.postcomment, name="postcomment"),
    path("getcomment/<int:post_id>", views.getcomment, name="getcomment"),
    path("following", views.following_posts, name="following"),
    path("editpost/<int:post_id>", views.edit_post, name="editpost"),
    path("like/<int:post_id>", views.like_post, name="like")
]
