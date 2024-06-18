from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View

from images.forms import ImageForm


@login_required
def dashboard_view(request):
    return render(request, 'images/dashboard_extension.html')


class ImageCreateView(LoginRequiredMixin, View):
    form_class = ImageForm
    template_name = 'images/image_upload.html'

    def get(self, request, *args, **kwargs):
        image_form = self.form_class()
        return render(request,
                      self.template_name,
                      {'image_form': image_form})

    def post(self, request, *args, **kwargs):
        image_form = self.form_class(data=request.POST,
                                     files=request.FILES)
        if image_form.is_valid():
            new_image = image_form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Dane zostały zaktualizowane')
        else:
            messages.error(request, 'Wystąpił błąd')
        return render(request,
                      self.template_name,
                      {'image_form': image_form})
