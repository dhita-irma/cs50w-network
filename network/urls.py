
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
    path("posts/<str:feed>", views.post_list, name="post-list"),
    path("follow/<int:pk>", views.follow, name="follow"),
]
