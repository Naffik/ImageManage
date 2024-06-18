from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, ListView

from images.forms import ImageForm
from images.models import Image
from images.utils import create_thumbnails


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
        return context


class ImageListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'images/image_list.html'
    context_object_name = 'images'
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by('-created_at')
