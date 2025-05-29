from django.urls import path
from .views import show_login, logout_view, register_view,dashboard_pengunjung,dashboard_dokter_hewan,dashboard_penjaga_hewan,dashboard_pelatih_hewan,dashboard_staf_admin

app_name = 'wajib' 

urlpatterns = [
    path('login/', show_login, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('pengunjung/', dashboard_pengunjung, name='dashboard_pengunjung'),
    path('dokter-hewan/', dashboard_dokter_hewan, name='dashboard_dokter_hewan'),
    path('penjaga-hewan/', dashboard_penjaga_hewan, name='dashboard_penjaga_hewan'), 
    path('pelatih-hewan/', dashboard_pelatih_hewan, name='dashboard_pelatih_hewan'),
    path('staf-admin/', dashboard_staf_admin, name='dashboard_staf_admin'),
    path('', dashboard_pengunjung, name='home'), 
]
