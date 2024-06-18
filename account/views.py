from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return redirect('login')

# def user_login(request):
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],
#                                 password=cd['password']
#                                 )
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authorized successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


@login_required()
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class EditView(LoginRequiredMixin, View):
    user_form_class = UserEditForm
    profile_form_class = ProfileEditForm
    template_name = 'account/edit.html'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class(instance=request.user)
        profile_form = self.profile_form_class(instance=request.user.profile)
        return render(request,
                      self.template_name,
                      {'user_form': user_form,
                       'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = self.user_form_class(instance=request.user,
                                         data=request.POST)
        profile_form = self.profile_form_class(instance=request.user.profile,
                                               data=request.POST,
                                               files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Dane zostały zaktualizowane')
        else:
            messages.error(request, 'Wystąpił błąd')
        return render(request,
                      self.template_name,
                      {'user_form': user_form,
                       'profile_form': profile_form})


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'users'
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/user_detail.html'
    context_object_name = 'user_detail'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', '')
        return context
