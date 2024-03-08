from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='')
    
    def __str__(self):
        return f'{self.name}'
    
class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(default='')
    starting_bid = models.FloatField(default=0)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, related_name='listing_by_category', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_auction')
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist')
    current_price = models.FloatField(default=0)
    winner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='win_auction', null=True)
    
    def __str__(self):
        return f'{self.title}'
    
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default='')
    bidding_price = models.FloatField(default=0)
    pass

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    pass
