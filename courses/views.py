from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Application, Profile, Review
from .forms import RegisterForm, ApplicationForm, ReviewForm, StatusUpdateForm


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
    reviews = Review.objects.filter(user=request.user)
    context = {
        'applications': applications,
        'reviews': reviews,
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


@login_required
def review_create(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    if application.status != Application.Status.COMPLETED:
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('dashboard')
    if hasattr(application, 'review'):
        messages.error(request, 'Вы уже оставили отзыв на эту заявку')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = application
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('dashboard')
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form, 'application': application})


def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.username != 'Admin26':
            messages.error(request, 'Доступ запрещён')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper


@manager_required
def manager_view(request):
    applications = Application.objects.select_related('user__profile').all()
    reviews = Review.objects.select_related('user', 'application').all()
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')
    if status_filter:
        applications = applications.filter(status=status_filter)
    allowed_sorts = ['created_at', '-created_at', 'start_date', '-start_date']
    if sort_by not in allowed_sorts:
        sort_by = '-created_at'
    applications = applications.order_by(sort_by)
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=application_id)
        form = StatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f'Статус заявки #{application.id} изменён на "{application.get_status_display()}"')
        return redirect(request.path_info)

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'status_choices': Application.Status.choices,
        'reviews': reviews,
    }
    return render(request, 'manager.html', context)