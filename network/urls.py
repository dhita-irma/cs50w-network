
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # API routes
    path("posts/", views.create_post, name="create-post"),
    path("posts/<int:pk>", views.post_detail, name="post-detail"),
    path("posts/<str:post_filter>", views.post_list, name="post-list"),

    path("<str:username>/<str:fol_type>", views.follow_list, name="follow-list"),
]
