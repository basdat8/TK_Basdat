from django.urls import path
from . import views

urlpatterns = [
    path('catatanmedis/', views.list_catatan_medis, name='list_catatan_medis'),
    path('catatanmedis/add/', views.add_catatan_medis, name='catatanmedis-add'),
]