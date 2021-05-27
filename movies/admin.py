from django.contrib import admin
from .models import Movie

# Register your models here.
class MovieAdmin(admin.ModelAdmin) :
    list_display = ("id", "title", "release_date", "vote_count", "vote_average", )
    
    class Meta :
        verbose_name_plural = "영화"

admin.site.register(Movie, MovieAdmin)
admin.site.site_title = "영화"