from django.contrib import admin
from .models import User, Post, PostEdition, Like, LikeChange, Follow, FollowChange, Comment, CommentChange

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    list_editable = ("username", "email")
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "content", "user")
    list_editable = ("content", "user")
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp", "likeUnlike", "post")
    list_editable = ("user", "post")
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "userPointer", "userTarget")
    list_editable = ("userPointer", "userTarget")
class PostChangeAdmin(admin.ModelAdmin):
    list_display=("id", "content", "timestamp", "post")
class LikeChangeAdmin(admin.ModelAdmin):
    list_display=("id", "likeUnlike", "timestamp")

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(PostEdition, PostChangeAdmin)
admin.site.register(LikeChange, LikeChangeAdmin)
