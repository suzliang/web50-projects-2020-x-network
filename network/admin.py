from django.contrib import admin
from .models import *

# Register your models here.
class FollowingAdmin(admin.ModelAdmin):
    filter_horizontal = ("following","followers",)
class LikeAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("comments",)

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment)