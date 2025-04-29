from django.shortcuts import render, get_object_or_404, redirect
from .models import Atraksi
from .forms import AtraksiForm

def daftar_atraksi(request):
    atraksi = Atraksi.objects.all()
    return render(request, 'atraksi/daftar.html', {'atraksi': atraksi})

def tambah_atraksi(request):
    if request.method == 'POST':
        form = AtraksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daftar_atraksi')
    else:
        form = AtraksiForm()
    return render(request, 'atraksi/form.html', {'form': form, 'judul': 'Form Tambah Atraksi'})

def edit_atraksi(request, id):
    atraksi = get_object_or_404(Atraksi, id=id)
    if request.method == 'POST':
        form = AtraksiForm(request.POST, instance=atraksi)
        if form.is_valid():
            form.save()
            return redirect('daftar_atraksi')
    else:
        form = AtraksiForm(instance=atraksi)
    return render(request, 'atraksi/form.html', {'form': form, 'judul': 'Form Edit Atraksi'})

def hapus_atraksi(request, id):
    atraksi = get_object_or_404(Atraksi, id=id)
    if request.method == 'POST':
        atraksi.delete()
        return redirect('daftar_atraksi')
    return render(request, 'atraksi/konfirmasi_hapus.html', {'atraksi': atraksi})
