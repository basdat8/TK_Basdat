from django.urls import path
from . import views
app_name = 'adopsi'

urlpatterns = [
    path('', views.adopsi_view, name='umum'),
    path('staff',views.adopsi_staff_view , name = 'staff'),
    path('update/<uuid:hewan_id>/', views.update_adopsi, name='update'),
    path('delete/<uuid:hewan_id>/', views.delete_adopsi, name='delete'),
    path('verifikasi/<str:username>/', views.verifikasi_adopter, name='verifikasi'),
]
