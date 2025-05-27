from django import forms
from .models import Atraksi

class AtraksiForm(forms.ModelForm):
    class Meta:
        model = Atraksi
        fields = ['nama', 'lokasi', 'kapasitas', 'jadwal', 'pelatih', 'hewan']
        widgets = {
            'jadwal': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'pelatih': forms.CheckboxSelectMultiple,
            'hewan': forms.CheckboxSelectMultiple,
        }
