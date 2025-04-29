from django import forms
from django.contrib.auth.models import User
from .models import Pengunjung, DokterHewan, Staf

"""

# Form umum untuk User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")

        return cleaned_data


# Form Registrasi Pengunjung
class PengunjungForm(forms.ModelForm):
    class Meta:
        model = Pengunjung
        fields = ['alamat', 'tgl_lahir', 'no_telp']


# Form Registrasi Dokter Hewan
class DokterHewanForm(forms.ModelForm):
    spesialisasi = forms.ChoiceField(choices=[
        ('mamalia_besar', 'Mamalia Besar'),
        ('reptil', 'Reptil'),
        ('burung_eksotis', 'Burung Eksotis'),
        ('primata', 'Primata'),
        ('lainnya', 'Lainnya')
    ])

    class Meta:
        model = DokterHewan
        fields = ['no_STR', 'spesialisasi']


# Form Registrasi Staf
class StafForm(forms.ModelForm):
    peran = forms.ChoiceField(choices=[
        ('penjaga_hewan', 'Penjaga Hewan'),
        ('staf_administrasi', 'Staf Administrasi'),
        ('pelatih_pertunjukan', 'Pelatih Pertunjukan')
    ])

    class Meta:
        model = Staf
        fields = ['peran', 'id_staf']
"""