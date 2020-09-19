from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserFollowing


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']


def index(request):
    return render(request, "network/index.html", {
        'form': PostForm(), 
    })


def post_list(request, post_filter):

    # Return all posts 
    if post_filter == "all":
        posts = Post.objects.all()

    # Return posts by following users 
    elif post_filter == "following":
        if request.user.is_authenticated:
            following = request.user.following.all()
            following_list = [follow.following_user.id for follow in following]
            posts = Post.objects.filter(creator__in=following_list)
        else:
            return JsonResponse({"error": f"You need to log in."}, status=401)
    
    # Return posts by a specific user
    else:
        try: 
            user = User.objects.get(username=post_filter)
            posts = Post.objects.filter(creator=user.id)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User '{post_filter}' not found."}, status=404)
    
    # Return posts in reverse chronological order 
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def post_detail(request, pk):
    # Query for requested post
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": f"Post id {pk} not found."}, status=404)

    # Return post contents
    if request.method == 'GET':
        return JsonResponse(post.serialize())

    # Post must be via GET
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    #TODO: implement LIKE 


def follow_list(request, username, fol_type):

    # Query for requested user
    try: 
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User {username} not found."}, status=404)

    # Get follow list
    follow_list = []
    if request.method == 'GET':

        if fol_type == 'following':
            fols = user.following.all()
            for i in range(len(fols)):
                follow_list.append(fols[i].following_user.username)

            data = {
                "user": username,
                "following": follow_list
            }

        elif fol_type == 'followers':
            fols = user.followers.all()

            for i in range(len(fols)):
                follow_list.append(fols[i].user.username)

            data = {
                "user": username,
                "followers": follow_list
            }

        else:
            return JsonResponse({"error": "Only 'following' or 'followers' parameter accepted."}, status=400)

        # Return JSON Response 
        return JsonResponse(data, safe=False)

    # Post must be via GET
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


@login_required
def create_post(request):

    # Create new post must be via POST 
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    form = PostForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        user = request.user
        new = Post(content=content, user=user)
        new.save()
        return HtttpResponse("New Post created")
        

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
