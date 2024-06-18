from django.contrib import admin
from .models import Profile, AccountTier


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumbnail_size', 'original_link', 'expiring_link']

