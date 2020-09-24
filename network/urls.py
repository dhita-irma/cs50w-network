
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # API routes
    path("posts/", views.create_post, name="create-post"),
    path("posts/<str:feed>", views.post_list, name="post-list"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<int:pk>", views.follow, name="follow"),
]
