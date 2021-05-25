from django.contrib import admin
from .models import Movie

# Register your models here.
class MovieAdmin(admin.ModelAdmin) :
    list_display = ("id", "title", "release_date", "vote_count", "vote_average", )

admin.site.register(Movie, MovieAdmin)