import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Post, User


def index(request):
    return render(request, "network/index.html")


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


def new(request):

    # New post must be submitted via POST
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)
    
    # Check post for content
    data = request.body.decode()
    if not data:
        return JsonResponse({'error': 'Post needs content'}, status=400)

    # Save post
    post = Post(poster=request.user, text=data, timestamp=timezone.now())
    post.save()
    
    return JsonResponse({'message': 'New post added'}, status=201)


def posts(request):
    
    # Get id of last post
    last_post_id = Post.objects.aggregate(Max('id'))['id__max']
    if last_post_id:

        # Get corresponding ids of start and end posts to be in reverse-chronological order
        start = int(request.GET.get('start') or 0)
        end = int(request.GET.get('end') or start + 9)

        top_post_id = (last_post_id + 1) - start
        bottom_post_id = (last_post_id + 1) - end
        if bottom_post_id < 0:
            bottom_post_id = last_post_id + 1 - top_post_id

        requested_posts = Post.objects.filter(id__lte=top_post_id, id__gte=bottom_post_id)
        reverse_chronological_posts = [post.dictify() for post in sorted(requested_posts, key= lambda post: post.timestamp, reverse=True)]
       
        return JsonResponse({
            'posts': reverse_chronological_posts
        })

    else:
        return JsonResponse({
            'posts': 'No posts yet'
        })


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
