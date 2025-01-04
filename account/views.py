from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models



# Create your views here.


def log_in(request):
    if request.user.is_authenticated:
        return redirect('home:main')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home:main')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home:main')


def register(request):
    if request.user.is_authenticated:
        return redirect('home:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                            last_name=lastname)
            user.save()
            return redirect('account:login')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home:main')
    else:
        form = EditProfileForm(instance=request.user, user=request.user)

    return render(request, 'account/edit_profile.html', {'form': form})

def about_developer(request):
    user = get_object_or_404(models.Profile, id=3)
    return render(request, 'account/about_developer.html', {'admin': user})


