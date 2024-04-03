from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from datetime import datetime

def index(request):
    if request.method == 'POST':
        poster = request.user
        content = request.POST['content']
        timestamp = datetime.now()
        new_post = Post(poster=poster, content=content, timestamp=timestamp)
        new_post.save()    

    return render(request, "network/index.html", {
        'all_post': Post.objects.all(),
    })

def profile(request, username):
    
    followed_user = User.objects.get(username=username)
    following_user = request.user
    relationship = FollowingRelationship(followed_user=followed_user, following_user=following_user)
    
    if request.method == 'POST':
        
        if request.POST.get('follow_unfollow','') == 'Follow':
            relationship.save()
        elif request.POST.get('follow_unfollow','') == 'Unfollow':
            FollowingRelationship.objects.filter(followed_user=followed_user, following_user=following_user).delete()

    
    return render(request, 'network/profile.html', {
        'selected_user': User.objects.get(username=username),
        'is_following': relationship in FollowingRelationship.objects.all(),
    })

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
