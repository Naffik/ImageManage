from django import forms
from django.contrib.auth.models import User
from images.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('original_image',)
