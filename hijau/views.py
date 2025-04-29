from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CatatanMedis

# Create your views here.

class CatatanMedisListView(ListView):
    model = CatatanMedis
    template_name = 'catatanmedis_list.html'
    context_object_name = "catatanmedis"

class CatatanMedisCreateView(CreateView):
    model = CatatanMedis
    fields = '__all__'
    template_name = 'catatanmedis_form.html'
    success_url = reverse_lazy('catatanmedis_list')

class CatatanMedisUpdateView(UpdateView):
    model = CatatanMedis
    fields = '__all__'
    template_name = 'catatanmedis_form.html'
    success_url = reverse_lazy('catatanmedis_list')

class CatatanMedisDeleteView(DeleteView):
    model = CatatanMedis
    template_name = 'catatanmedis_delete.html'
    success_url = reverse_lazy('catatanmedis_list')
