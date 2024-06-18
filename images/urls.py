from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard_view, ImageCreateView, ImageDetailView, ImageListView

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('image_upload/', ImageCreateView.as_view(), name='image_upload'),
    path('image_detail/<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('image_list/', ImageListView.as_view(), name='image_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
