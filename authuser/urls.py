from django.urls import path
from . views import show_login, logout_view, pilih_role_view, form_pengguna_view, form_dokterhewan_view, form_staff_view, dashboard_pengunjung,dashboard_dokter_hewan,dashboard_penjaga_hewan,dashboard_pelatih_hewan,dashboard_staf_admin

app_name = 'wajib' 

urlpatterns = [
    path('login/', show_login, name='login'),
    path('logout/', logout_view, name='logout'),

    path('register/', pilih_role_view, name='pilih_role'),
    path('register/pengguna/', form_pengguna_view, name='form_pengguna'),
    path('register/dokter-hewan/', form_dokterhewan_view, name='form_dokterhewan'),
    path('register/staff/', form_staff_view, name='form_staff'),

    path('pengunjung/', dashboard_pengunjung, name='dashboard_pengunjung'),
    path('dokter-hewan/', dashboard_dokter_hewan, name='dashboard_dokter_hewan'),
    path('penjaga-hewan/', dashboard_penjaga_hewan, name='dashboard_penjaga_hewan'), 
    path('pelatih-hewan/', dashboard_pelatih_hewan, name='dashboard_pelatih_hewan'),
    path('staf-admin/', dashboard_staf_admin, name='dashboard_staf_admin'),
    path('', dashboard_pengunjung, name='home'), 
]
