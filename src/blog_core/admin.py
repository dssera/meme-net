from django.contrib import admin
from .models import Post, Image, Comment

admin.site.register((Post, Image, Comment))
