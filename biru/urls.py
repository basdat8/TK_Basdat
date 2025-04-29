from django.urls import path
from . import views

urlpatterns = [
    path('atraksi/', views.list_atraksi, name='list_atraksi'),
    path('atraksi/tambah/', views.tambah_atraksi, name='tambah_atraksi'),
    path('atraksi/<uuid:id>/edit/', views.edit_atraksi, name='edit_atraksi'),
    path('atraksi/<uuid:id>/hapus/', views.hapus_atraksi, name='hapus_atraksi'),
]
