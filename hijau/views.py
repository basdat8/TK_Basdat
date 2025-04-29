from django.shortcuts import render, redirect
from django.db import connection



# Create your views here.

def list_catatan_medis(request):
    return render(request, 'catatanmedis_list.html', {})

def add_catatan_medis(request):
    return render(request, 'catatanmedis_form.html', {})

def edit_catatan_medis(request):
    return render(request, 'catatanmedis_edit.html', {})


