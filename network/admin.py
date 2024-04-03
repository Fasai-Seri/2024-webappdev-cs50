from django.contrib import admin

from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FollowingRelationship)