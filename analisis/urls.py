import os
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
  
    path('', views.menu_general, name='menu_general'),
    
    path('loading/<str:url>/', views.loading_screen, name='loading_screen_simple'),
    path('loading/<str:url>/<str:method>/', views.loading_screen, name='loading_screen'),

  
    path('ordenamiento/', views.menu_ordenamiento, name='menu_ordenamiento'),
    path('ordenamiento/sort/<str:method>/<int:tipo>', views.sort, name='sort_books'),
  
    path('analisis/', views.menu_analysis_methods, name='menu_analysis_methods'),
    path('analisis/frecuencia/', views.analizar_frecuencia, name='analizar_frecuencia'),
    path('analisis/dendograma/', views.mostrar_dendograma, name='mostrar_dendograma'),
    path('analisis/nube-palabras/', views.mostrar_nube_palabras, name='mostrar_nube_palabras'),
    path('analisis/graficas-frecuencia/', views.graficas_frecuencia, name='graficas_frecuencia'),
    path('analisis/graficas-grafo/', views.mostrar_grafo, name='mostrar_grafo'),

    path('generar/dendograma/', views.generar_dendograma, name='generar_dendograma'),
    path('generar/nube-palabras/', views.generar_nube_palabras, name='generar_nube_palabras'),
    path('generar/graficas-frecuencia/', views.generar_graficas_frecuencia, name='generar_graficas_frecuencia'),
    path('generar/graficas-grafo/', views.generar_grafo, name='generar_grafo'),

]