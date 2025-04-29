from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListView.as_view(), name='catatanmedis-list'),
    path('add/', views.CreateView.as_view(), name='catatanmedis-add'),
    path('edit/<int:pk>/', views.UpdateView.as_view(), name='catatanmedis-edit'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='catatanmedis-delete'),
]