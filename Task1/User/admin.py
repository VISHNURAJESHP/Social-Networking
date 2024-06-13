from django.contrib import admin
from .models import user,FriendRequest 

@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name','password') 

@admin.register(FriendRequest)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','from_user', 'to_user', 'status', 'created_at')
