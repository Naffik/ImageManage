import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, ListView

from core import settings
from images.forms import ImageForm
from images.models import Image, Thumbnail
from images.utils import create_thumbnails


@login_required
def dashboard_view(request):
    readme_path = os.path.join(settings.BASE_DIR, 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()
    return render(request,
                  'images/dashboard_extension.html',
                  {'readme_content': readme_content})


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
        if 'original_image' in request.FILES:
            file_name, image_extension = os.path.splitext(request.FILES['original_image'].name)
            if len(file_name) > 50:
                request.FILES['original_image'].name = file_name[:50] + image_extension
        if image_form.is_valid():
            new_image = image_form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_thumbnails(new_image, request.FILES['original_image'])
            messages.success(request, 'Dane zostały zaktualizowane')
        else:
            messages.error(request, 'Wystąpił błąd')
        return render(request,
                      self.template_name,
                      {'image_form': image_form})


class ImageDetailView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'images/image_detail.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', '')

        user_profile = self.request.user.profile
        if user_profile:
            context['account_tier'] = user_profile.account_tier
            context['original_link'] = user_profile.account_tier.original_link
            context['expiring_link'] = user_profile.account_tier.expiring_link

        thumbnails = Thumbnail.objects.filter(image=context['image'])
        if thumbnails:
            context['thumbnails'] = thumbnails
        return context


class ImageListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'images/image_list.html'
    context_object_name = 'images'
    paginate_by = 14

    def get_queryset(self):
        return Image.objects.prefetch_related('thumbnails').filter(user=self.request.user).order_by('-created_at')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     thumbnails = []
    #     for image in context['images']:
    #         thumbnails.append(Thumbnail.objects.filter(image=image)[:1])
    #     print(thumbnails.thumbnail)
    #     if thumbnails:
    #         context['thumbnails'] = thumbnails
    #     return context
