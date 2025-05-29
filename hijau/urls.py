from django.urls import path
from . import views

urlpatterns = [
    path('catatanmedis/', views.list_catatan_medis, name='list_catatan_medis'),
    path('catatanmedis/add/', views.add_catatan_medis, name='add_catatan_medis'),
    path('catatanmedis/edit/', views.edit_catatan_medis, name='edit_catatan_medis'),
    path('catatanmedis/delete/', views.delete_catatan_medis, name='hapus_catatan_medis'),
    path('jadwalpemeriksaan/', views.list_jadwal_pemeriksaan, name='list_jadwal_pemeriksaan'),
    path('jadwalpemeriksaan/add/', views.add_jadwal_pemeriksaan, name='add_jadwal_pemeriksaan'),
    path('jadwalpemeriksaan/edit/', views.edit_jadwal_pemeriksaan, name='edit_jadwal_pemeriksaan'),
    path('jadwalpemeriksaan/delete/', views.delete_jadwal_pemeriksaan, name='hapus_jadwal_pemeriksaan'),
    path('pemeriksaan/', views.list_pemeriksaan, name='list_pemeriksaan'),
]