from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('create/', views.create_task, name='create_task'),
    path('register/', views.register, name='register'),
    path('toggle/<int:pk>/', views.toggle_complete, name='toggle_complete'),
    path('api/tasks/', views.task_api, name='task_api'),
    path('api/tasks/<int:pk>/', views.task_detail_api, name='task_detail_api'),
]
