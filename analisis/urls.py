import os
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
  
    path('', views.menu_general, name='menu_general'),
    
  
    path('ordenamiento/', views.menu_ordenamiento, name='menu_ordenamiento'),
    path('ordenamiento/loading/<str:method>/', views.loading_screen, name='loading_screen'),
    path('ordenamiento/sort/<str:method>/', views.sort, name='sort_books'),
  
    path('analisis/', views.menu_analysis_methods, name='menu_analysis_methods'),
    path('analisis/frecuencia/', views.analizar_frecuencia, name='analizar_frecuencia'),
    path('analisis/dendograma/', views.generar_dendograma, name='generar_dendograma'),
    path('analisis/nube-palabras/', views.generar_nube_palabras, name='generar_nube_palabras'),
    path('analisis/graficas-frecuencia/', views.graficas_frecuencia, name='graficas_frecuencia'),
]