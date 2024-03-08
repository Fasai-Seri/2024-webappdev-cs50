from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Category, AuctionListing

class CreateLisingForm(forms.Form):
    title = forms.CharField(label='Title:')
    description = forms.CharField(widget=forms.Textarea(), label='Description:')
    starting_bid = forms.FloatField(label='Starting bid:')
    image_url = forms.URLField(required=False, label='URL for image (optional):')
    category = forms.ChoiceField(widget=forms.Select, choices=[(cat.name, cat.name) for cat in Category.objects.all()], initial=('No category'))
        
def index(request):
    return render(request, "auctions/index.html", {
        'active_listing': AuctionListing.objects.filter(is_active=True),
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):
    if request.method == 'POST':
        form = CreateLisingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            category = Category.objects.get(name=form.cleaned_data['category'])
            owner = request.user
            is_active = True
            new_listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, owner=owner, is_active=is_active)
            new_listing.save()
        
           
    return render(request, 'auctions/create_listing.html', {
        'form': CreateLisingForm(),
    })
    
def listing_page(request, id):
    if request.method == 'POST':
        add_remove = request.POST.get('add_remove')
        if add_remove == 'add':
            AuctionListing.objects.get(id=id).watchlist.add(request.user)
        else:
            AuctionListing.objects.get(id=id).watchlist.remove(request.user)
                            
    return render(request, 'auctions/listing_page.html',{
        'selected_listing': AuctionListing.objects.get(id=id),
        'user': request.user,
    })

def watchlist(request):
    return render(request, 'auctions/watchlist.html', {
        'all_watchlist': request.user.watchlist.all()
    })
