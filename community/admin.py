from django.contrib import admin
from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin) :
    list_display = ("user", "title", "content", "movie", "created_at", )

admin.site.register(Review, ReviewAdmin)