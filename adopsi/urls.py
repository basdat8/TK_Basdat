from django.urls import path
from . import views
app_name = 'adopsi'

urlpatterns = [
    path('', views.adopsi_view, name='umum'),
    path('staff',views.adopsi_staff_view , name = 'staff')
]
