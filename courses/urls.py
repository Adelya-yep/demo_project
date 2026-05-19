from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/new/', views.application_create, name='application_create'),
    path('applications/<int:application_id>/review/', views.review_create, name='review_create'),
    path('manager/', views.manager_view, name='manager'),
]
