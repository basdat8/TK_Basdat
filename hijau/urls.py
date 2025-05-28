from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_catatan_medis, name='list_catatan_medis'),
    path('add/', views.add_catatan_medis, name='add_catatan_medis'),
    path('edit/<uuid:id>/', views.edit_catatan_medis, name='edit_catatan_medis'),
    path('delete/<uuid:id>/', views.delete_catatan_medis, name='hapus_catatan_medis'),
]