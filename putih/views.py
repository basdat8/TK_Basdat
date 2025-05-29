import uuid

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
"""from .forms import UserRegistrationForm

from .forms import UserRegistrationForm, PengunjungForm, DokterHewanForm, StafForm"""
from django.views.generic import TemplateView



# Create your views here.
class IndexView(TemplateView):
    template_name = 'putih/index.html'


def index(request):
    return render(request, 'putih/index.html')

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

"""
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Ambil peran yang dipilih
            role = request.POST.get('role')

            if role == 'pengunjung':
                pengunjung_form = PengunjungForm(request.POST)
                if pengunjung_form.is_valid():
                    pengunjung = pengunjung_form.save(commit=False)
                    pengunjung.pengguna = user
                    pengunjung.save()

            elif role == 'dokter_hewan':
                dokter_form = DokterHewanForm(request.POST)
                if dokter_form.is_valid():
                    dokter = dokter_form.save(commit=False)
                    dokter.pengguna = user
                    dokter.spesialisasi = dokter_form.cleaned_data['spesialisasi']
                    dokter.save()

            elif role == 'staf':
                staf_form = StafForm(request.POST)
                if staf_form.is_valid():
                    staf = staf_form.save(commit=False)
                    staf.pengguna = user
                    staf.peran = staf_form.cleaned_data['peran']
                    staf.id_staf = generate_staff_id(staf.peran)  # Fungsi untuk generate ID staf
                    staf.save()

            # Login user setelah registrasi
            login(request, user)

            # Redirect ke halaman dashboard
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'user_form': user_form})


def generate_staff_id(peran):
    # Fungsi untuk generate id staf berdasarkan peran
    if peran == 'penjaga_hewan':
        return 'PH-' + str(uuid.uuid4())
    elif peran == 'staf_administrasi':
        return 'SA-' + str(uuid.uuid4())
    elif peran == 'pelatih_pertunjukan':
        return 'PP-' + str(uuid.uuid4())
    return str(uuid.uuid4())
"""

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'pengunjung'):
            # Pengunjung
            return render(request, 'dashboard/pengunjung.html')
        elif hasattr(request.user, 'dokterhewan'):
            # Dokter Hewan
            return render(request, 'dashboard/dokter_hewan.html')
        elif hasattr(request.user, 'staf'):
            # Staf
            return render(request, 'dashboard/staf.html')
    else:
        return redirect('login')




