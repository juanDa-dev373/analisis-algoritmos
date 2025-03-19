import os
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.menu_ordenamiento, name='menu_ordenamiento'),
    path('loading/<str:method>/', views.loading_screen, name='loading_screen'),
    path('sort/<str:method>/', views.sort, name='sort_books'),
]