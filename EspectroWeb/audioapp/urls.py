from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio
    path('procesar_audio/', views.procesar_audio_view, name='procesar_audio'),  # Ruta de procesamiento de audio
]
