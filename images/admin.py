from django.contrib import admin

from images.models import Image, Thumbnail, ExpirationLink

# Register your models here.

admin.site.register(Image)
admin.site.register(Thumbnail)
admin.site.register(ExpirationLink)
