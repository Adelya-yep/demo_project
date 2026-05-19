from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Application, Profile
from .forms import RegisterForm


def index(request):
    return render(request, 'index.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    applications = Application.objects.filter(user=request.user)
    context = {
        'applications': applications,
    }
    return render(request, 'dashboard.html', context)


@login_required
def application_create(request):
    if request.user.username == 'Admin26':
        messages.error(request, 'Администратор не может создавать заявки')
        return redirect('manager')
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'application_form.html', {'form': form})