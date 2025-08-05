# Gasolina/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='gasolina_index'),
]
