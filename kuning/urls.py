from django.urls import path
from . import views

urlpatterns = [
    path('hewan/', views.list_hewan, name='list_hewan'),
    path('hewan/tambah/', views.tambah_hewan, name='tambah_hewan'),
    path('hewan/edit/<uuid:id>/', views.edit_hewan, name='edit_hewan'),
    path('hewan/hapus/<uuid:id>/', views.hapus_hewan, name='hapus_hewan'),
    path('habitat/', views.list_habitat, name='list_habitat'),
    path('habitat/tambah/', views.tambah_habitat, name='tambah_habitat'),
    path('habitat/edit/<str:nama>/', views.edit_habitat, name='edit_habitat'),
    path('habitat/hapus/<str:nama>/', views.hapus_habitat, name='hapus_habitat'),
    path('habitat/detail/<str:nama>/', views.detail_habitat, name='detail_habitat'),
]
