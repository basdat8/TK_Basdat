from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

"""path('register/', views.register, name='register')"""