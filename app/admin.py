from django.contrib import admin
from .models import Rubric, Post, FavoriteUserAnnouncements

admin.site.register(Rubric)
admin.site.register(Post)
admin.site.register(FavoriteUserAnnouncements)
