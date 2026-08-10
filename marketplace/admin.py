from django.contrib import admin
from .models import UserProfile, Category, Item

# Register your models here so they show up in the Django admin panel
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Item)