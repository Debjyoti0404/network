
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
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("following", views.following_posts, name="following"),
    path("editpost/<int:post_id>", views.edit_post, name="editpost")
]
