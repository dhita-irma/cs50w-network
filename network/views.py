import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserFollowing


def index(request):
    return render(request, "network/index.html")


def post_list(request, feed):
    """
    API returning posts JsonResponsed depending on 3 arguments: 
    'all' = return all posts 
    'following' = return posts by following users 
    '<username>' = return posts by user <username>

    """
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


@login_required
def create_post(request):
    """API to create post"""

    # Create new post must be via POST 
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    # Take JSON string and convert it to dict 
    data = json.loads(request.body)
    content = data.get("content", "")
    
    # Save post to database
    post = Post(content=content, creator=request.user)
    post.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)


@login_required
def follow(request, pk):
    """API to follow or unfollow user"""

    # Muust be via POST 
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    current_user = request.user
    target_user = User.objects.get(pk=pk)
    
    # Check if current user follow target user 
    if current_user not in target_user.get_followers():
        follow = UserFollowing(user=current_user, following_user=target_user)
        follow.save()
        return JsonResponse({"message": "Follow user successfully."}, status=201)
    else: 
        f = UserFollowing.objects.get(user=current_user, following_user=target_user)
        f.delete()
        f.save()
        return JsonResponse({"message": "Unfollow user successfully."}, status=201)
        

def profile(request, username):
    """API returning user profile"""

    # Query for requested user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User {username} not found."}, status=404)

    # Return JSON response
    if request.method == 'GET':
        return JsonResponse(user.serialize())
    else:
        return JsonResponse({"error": "GET request required."}, status=400)


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
