"""
URL configuration for SGTAreas2_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.views import login_view, registro_view, tareas_view, nueva_tarea_view, modificar_tarea_view

urlpatterns = [
    path('', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('tareas/', tareas_view, name='tareas'),
    path('nueva_tarea/', nueva_tarea_view, name='nueva_tarea'),
    path('modificar_tarea/<int:tarea_id>/', modificar_tarea_view, name='modificar_tarea'),
]
