from django.contrib import admin

from .models import Category, AuctionListing, User
# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchlist',)
    
admin.site.register(Category)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(User)