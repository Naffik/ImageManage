from django import forms
from django.forms import FileInput
from django.contrib.auth.models import User
from images.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('original_image',)
        labels = {'original_image': 'Image'}
        widgets = {
            'name': FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
        }
