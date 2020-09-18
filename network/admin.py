from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "content")


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
