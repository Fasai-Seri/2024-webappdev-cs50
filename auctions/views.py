from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Category, AuctionListing, Bid, Comment

class CreateLisingForm(forms.Form):
    title = forms.CharField(label='Title:')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':45}), label='Description:')
    starting_bid = forms.FloatField(label='Starting bid:')
    image_url = forms.URLField(required=False, label='URL for image (optional):')
    category = forms.ChoiceField(widget=forms.Select, choices=[(cat.name, cat.name) for cat in Category.objects.all()], initial=('No category'))

class CreateBiddingForm(forms.Form):
    bidding_price = forms.FloatField(label='Bidding Price:')
    
class CreateCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':45}), label='Add your comment:')
    
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
            new_listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, owner=owner, is_active=is_active, current_price=0)
            new_listing.save()
        
           
    return render(request, 'auctions/create_listing.html', {
        'form': CreateLisingForm(),
    })
    
def listing_page(request, id):
    selected_listing = AuctionListing.objects.get(id=id)
    user = request.user
    if request.method == 'POST':
        add_remove = request.POST.get('add_remove')
        if add_remove == 'add to watchlist':
            selected_listing.watchlist.add(user)
        else:
            selected_listing.watchlist.remove(user)
            
        form = CreateBiddingForm(request.POST)
        if form.is_valid():
            bidding_price = form.cleaned_data['bidding_price']
            if bidding_price > selected_listing.current_price and bidding_price >= selected_listing.starting_bid:
                selected_listing.current_price = bidding_price
                selected_listing.winner = user
                selected_listing.save()
                bidder = user
                new_bidding = Bid(bidder=bidder, auction_listing=selected_listing, bidding_price=bidding_price)
                new_bidding.save()
            else:
                return render(request, 'auctions/listing_page.html', {
                    'selected_listing': AuctionListing.objects.get(id=id),
                    'user': request.user,
                    'bid_form': CreateBiddingForm(),
                    'comment_form': CreateCommentForm(),
                    'all_comment': AuctionListing.objects.get(id=id).from_listing.all(),
                    'warning': 'Your bid is lower than current price. Try again.'
                })
            
        close_auction = request.POST.get('close_auction')
        if close_auction == 'close this auction':
            selected_listing.is_active = False
            selected_listing.save()
            return HttpResponseRedirect(reverse('index'))
        
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            new_comment = Comment(commenter=user, auction_listing=selected_listing, comment=comment)
            new_comment.save()
            return HttpResponseRedirect(reverse('listing_page', args=[id]))
            
    return render(request, 'auctions/listing_page.html',{
        'selected_listing': AuctionListing.objects.get(id=id),
        'user': request.user,
        'bid_form': CreateBiddingForm(),
        'comment_form': CreateCommentForm(),
        'all_comment': AuctionListing.objects.get(id=id).from_listing.all()
    })

def watchlist(request):
    return render(request, 'auctions/watchlist.html', {
        'all_watchlist': request.user.watchlist.all()
    })
    
def all_category(request):
    return render(request, 'auctions/all_category.html', {
        'all_category': Category.objects.all()
    })
    
def listing_by_category(request, category_name):
    return render(request, 'auctions/listing_by_category.html', {
        'all_listing': Category.objects.get(name=category_name).listing_by_category.filter(is_active=True),
        'category_name': category_name
    })
