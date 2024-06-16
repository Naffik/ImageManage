from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<slug:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('edit/', views.EditView.as_view(), name='edit'),
]
