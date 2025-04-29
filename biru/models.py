from django.db import models

class Pelatih(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Hewan(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Atraksi(models.Model):
    nama = models.CharField(max_length=200)
    lokasi = models.CharField(max_length=200)
    kapasitas = models.IntegerField()
    jadwal = models.TimeField()
    pelatih = models.ManyToManyField(Pelatih)
    hewan = models.ManyToManyField(Hewan)
