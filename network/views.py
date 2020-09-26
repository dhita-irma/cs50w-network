import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserFollowing, Like


def index(request):
    """Render homepage displaying posts by all users."""

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "title": "Home",
        "posts": posts,
        "page_obj": page_obj
    })


@login_required
def following_posts(request):
    """Render page displaying posts by all followed accounts."""

    following = request.user.following.all()
    following_list = [follow.following_user.id for follow in following]

    # Filter posts created by followed accounts
    posts = Post.objects.filter(creator__in=following_list)
    
    return render(request, "network/index.html", {
        "title": "Following",
        "posts": posts
    })


@login_required
def create_post(request):

    # Create new post must be via POST 
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    # Take JSON string and convert it to dict 
    data = json.loads(request.body)
    content = data.get("content", "")
    
    # Save post to database
    post = Post(content=content, creator=request.user)
    post.save()

    return JsonResponse({
        "message": "Post sent successfully.",
        "post_id": post.id
    }, status=201)


def post(request, pk):
    """API returning post detail and update/edit post"""

    # Query for requested post
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": f"Post id {pk} not found."}, status=404)

    # Return post details
    if request.method == 'GET':
        return JsonResponse(post.serialize())
    
    # Edit post content
    elif request.method == 'PUT':
        data = json.loads(request.body)

        if data.get("content") is not None:
            post.content = data["content"]
            post.save()
            return JsonResponse({"message": "Post updated successfully."}, status=200)
        return JsonResponse({"error": "Post content cannot be None."}, status=404)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def like(request, pk):

    # Must be via POST 
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    current_user = request.user
    post = Post.objects.get(pk=pk)

    # Check if current user like post
    if current_user not in post.liked_by():
        like = Like(user=current_user, post=post)
        like.save()
        return JsonResponse({
            "message": "Like post successfully.",
            "like_count": post.like_count()
        }, status=200)
    else: 
        unlike = Like.objects.get(user=current_user, post=pk)
        unlike.delete()
        return JsonResponse({
            "message": "Unlike post successfully.",
            "like_count": post.like_count()
        }, status=200)


def profile_view(request, username):
    """Render page displaying user profile"""

    try: 
        profile = User.objects.get(username=username)
        posts = Post.objects.filter(creator=profile.id)
        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except User.DoesNotExist:
        return render(request, "network/error.html")

    return render(request, "network/profile.html", {
        "title": username,
        "profile": profile,
        "posts": posts,
        "page_obj": page_obj
    })


@login_required
def follow(request, pk):
    
    # Muust be via POST 
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    current_user = request.user
    target_user = User.objects.get(pk=pk)
    
    # Check if current user follow target user 
    if current_user not in target_user.get_followers():
        f = UserFollowing(user=current_user, following_user=target_user)
        f.save()
        return JsonResponse({
            "message": "Follow user successfully.",
            "followers_count": len(target_user.get_followers())
        }, status=200)
    else: 
        f = UserFollowing.objects.get(user=current_user, following_user=target_user)
        print(f)
        f.delete()
        return JsonResponse({
            "message": "Unfollow user successfully.",
            "followers_count": len(target_user.get_followers())
        }, status=200)


def post_list(request, feed):
    """API returning post list"""

    # Return all posts 
    if feed == "all":
        posts = Post.objects.all()

    # Return posts by following users 
    elif feed == "following":
        if request.user.is_authenticated:
            following = request.user.following.all()
            following_list = [follow.following_user.id for follow in following]
            posts = Post.objects.filter(creator__in=following_list)
        else:
            return JsonResponse({"error": f"You need to log in."}, status=401)
    
    # Return posts by a specific user
    else:
        try: 
            user = User.objects.get(username=feed)
            posts = Post.objects.filter(creator=user.id)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User '{feed}' not found."}, status=404)
    
    # Return posts in reverse chronological order 
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


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
