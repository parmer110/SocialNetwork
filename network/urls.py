from django.views.generic import RedirectView
from django.urls import path

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="/posts/allposts"), name="index"),
    path("posts", RedirectView.as_view(url="/posts/allposts"), name="index2"),
    path("following", RedirectView.as_view(url="/posts/following"), name="following"),
    path("profile/follow/<int:user_id>", views.follow, name="follow"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<str:current>/<int:user_id>", views.index, name="profile2"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<str:current>/", views.index),

    # API Routes
    path("msg", views.msgPost, name="post"),
    path("posts/edit", views.edit, name="edit"),
    path("posts/like", views.likeUnlike, name="like"),
]
