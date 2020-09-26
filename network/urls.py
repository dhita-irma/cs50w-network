
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following/", views.following_posts, name="following-posts"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("<str:username>", views.profile_view, name="profile"),

    # API routes
    path("posts/", views.create_post, name="create-post"),
    path("posts/<int:pk>", views.post, name="post-detail"),
    path("like/<int:pk>", views.like, name="like"),
    path("follow/<int:pk>", views.follow, name="follow"),
]
