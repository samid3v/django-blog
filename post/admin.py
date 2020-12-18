from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserImage, Category, Post, Comment

# Register your models here.
admin.site.register(UserImage)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
