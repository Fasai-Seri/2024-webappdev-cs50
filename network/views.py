import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



from .models import *
from datetime import datetime

def index(request):
    if request.method == 'POST':
        poster = request.user
        content = request.POST['content']
        posted_timestamp = datetime.now()
        new_post = Post(poster=poster, content=content, posted_timestamp=posted_timestamp)
        new_post.save()    

    all_post = Post.objects.all().order_by('-posted_timestamp')
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page_obj': page_obj
    })

def profile(request, username):
    
    selected_user = User.objects.get(username=username)
    all_post = Post.objects.filter(poster=selected_user).order_by('-posted_timestamp')
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.user.id == None:
        return render(request, 'network/profile.html', {
            'page_obj': page_obj,
            'selected_user': selected_user,
        })
        
    else:
        current_login_user = request.user
            
        if request.method == 'POST':
            relationship = FollowingRelationship(followed_user=selected_user, following_user=current_login_user)
            if request.POST.get('follow_unfollow','') == 'Follow':
                relationship.save()
            elif request.POST.get('follow_unfollow','') == 'Unfollow':
                FollowingRelationship.objects.filter(followed_user=selected_user, following_user=current_login_user).delete()
        
        return render(request, 'network/profile.html', {
            'page_obj': page_obj,
            'selected_user': selected_user,
            'is_following': FollowingRelationship.objects.filter(followed_user=selected_user, following_user=current_login_user),
            'following_number': len(FollowingRelationship.objects.filter(following_user=selected_user)),
            'followed_number': len(FollowingRelationship.objects.filter(followed_user=selected_user)),
        })
    
def following(request):
    followed_user = FollowingRelationship.objects.filter(following_user=request.user).values_list('followed_user')
    all_post = Post.objects.filter(poster__in=followed_user).order_by('-posted_timestamp')
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {
        'page_obj': page_obj,
    })

@csrf_exempt
@login_required
def post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        if data.get("add_like_user") is not None:
            post.like_user.add(request.user)
        if data.get("remove_like_user") is not None:
            post.like_user.remove(request.user)
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def my_posts(request):
    return JsonResponse([post.serialize() for post in Post.objects.filter(poster=request.user)], safe=False)
       
def like_posts(request):
    return JsonResponse([post.serialize() for post in request.user.liked_post.all()], safe=False)
    
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
