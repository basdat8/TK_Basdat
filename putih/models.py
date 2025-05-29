from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
import uuid



# Create your models here.
class Pengguna(AbstractUser):
    email = models.EmailField(unique=True)
    nama_depan = models.CharField(max_length=50)
    nama_tengah = models.CharField(max_length=50, blank=True, null=True)
    nama_belakang = models.CharField(max_length=50)
    no_telp = models.CharField(max_length=15)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Pengunjung(models.Model):
    pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True)
    alamat = models.CharField(max_length=200)
    tgl_lahir = models.DateField()

class DokterHewan(models.Model):
    pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True)
    no_STR = models.CharField(max_length=50)

class Spesialisasi(models.Model):
    dokter = models.ForeignKey(DokterHewan, on_delete=models.CASCADE)
    nama_spesialisasi = models.CharField(max_length=100)

    class Meta:
        unique_together = ('dokter', 'nama_spesialisasi')


class Staf(models.Model):
    id_staf = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True)
    class Meta:
        abstract = True

class PenjagaHewan(Staf):
    pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True)
    id_staf = models.UUIDField(default=uuid.uuid4)

class PelatihHewan(Staf):
    pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True)
    id_staf = models.UUIDField(default=uuid.uuid4)

class StafAdmin(Staf):
    pengguna = models.OneToOneField(Pengguna, on_delete=models.CASCADE, primary_key=True)
    id_staf = models.UUIDField(default=uuid.uuid4)

class Habitat(models.Model):
    nama = models.CharField(max_length=50, primary_key=True)
    luas_area = models.DecimalField(max_digits=10, decimal_places=2)
    kapasitas = models.IntegerField()
    status = models.CharField(max_length=100)


class Hewan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100, blank=True, null=True)
    spesies = models.CharField(max_length=100)
    asal_hewan = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(blank=True, null=True)
    status_kesehatan = models.CharField(max_length=50)
    nama_habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    url_foto = models.URLField(max_length=225)

class CatatanMedis(models.Model):
    hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    dokter = models.ForeignKey(DokterHewan, on_delete=models.CASCADE)
    tanggal_pemeriksaan = models.DateField()
    diagnosis = models.CharField(max_length=100, blank=True, null=True)
    pengobatan = models.CharField(max_length=100, blank=True, null=True)
    status_kesehatan = models.CharField(max_length=100)
    catatan_tindak_lanjut = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ("hewan", "tanggal_pemeriksaan")



class Pakan(models.Model):
    hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    jadwal = models.DateTimeField()
    jenis = models.CharField(max_length=50)
    jumlah = models.IntegerField()
    status = models.CharField(max_length=50)

    class Meta:
        unique_together = ('hewan', 'jadwal')

class Memberi(models.Model):
    hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    jadwal = models.DateTimeField()
    penjaga = models.ForeignKey(PenjagaHewan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hewan', 'jadwal', 'penjaga')


class Fasilitas(models.Model):
    nama = models.CharField(primary_key= True, max_length=50)
    jadwal = models.DateTimeField()
    kapasitas_max = models.IntegerField()

class Atraksi(models.Model):
    nama_atraksi = models.ForeignKey(Fasilitas, on_delete=models.CASCADE)
    lokasi = models.CharField(max_length=100)

class JadwalPenugasan(models.Model):
    pelatih = models.ForeignKey(PelatihHewan, on_delete=models.CASCADE)
    tgl_penugasan = models.DateTimeField()
    nama_atraksi = models.ForeignKey(Atraksi, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('pelatih', 'tgl_penugasan')

class Berpartisipasi(models.Model):
    nama_fasilitas = models.ForeignKey(Fasilitas, on_delete=models.CASCADE)
    id_hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nama_fasilitas', 'id_hewan')

class JadwalPemeriksaanKesehatan(models.Model):
    id_hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    tgl_pemeriksaan_selanjutnya = models.DateTimeField()
    freq_pemeriksaan_rutin = models.IntegerField()

    class Meta:
        unique_together = ('id_hewan', 'tgl_pemeriksaan_selanjutnya')


class Wahana(models.Model):
    nama_wahana = models.ForeignKey(Fasilitas, on_delete=models.CASCADE)
    peraturan = models.TextField()

class Adopter(models.Model):
    username_adopter = models.ForeignKey(Pengunjung, on_delete=models.CASCADE)
    id_adopter = models.UUIDField(default=uuid.uuid4)
    total_kontribusi = models.IntegerField()
    class Meta:
        unique_together = ('username_adopter', 'id_adopter')

class Individu(models.Model):
    nik = models.CharField(
        max_length=16,
        primary_key=True,
        validators=[MinLengthValidator(16), MaxLengthValidator(16)]
    )
    nama = models.CharField(max_length=100)
    adopter = models.ForeignKey('Adopter', on_delete=models.CASCADE)

class Organisation(models.Model):
    npp = models.CharField(
        max_length=8,
        primary_key=True,
        validators=[MinLengthValidator(8), MaxLengthValidator(8)]
    )
    nama_organisation = models.CharField(max_length=100)
    id_adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)

class Adopsi(models.Model):
    id_adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    id_hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    status_pembayaran = models.CharField(max_length=10)
    tgl_mulai_adopsi = models.DateTimeField()
    tgl_berhenti_adopsi = models.DateTimeField()
    kontribusi_finansial = models.IntegerField()
    class Meta:
        unique_together = ('id_adopter', 'id_hewan', 'tgl_mulai_adopsi')

class Reserasi(models.Model):
    username_p = models.ForeignKey(Pengunjung, on_delete=models.CASCADE)
    nama_atraksi = models.ForeignKey(Atraksi, on_delete=models.CASCADE)
    tanggal_kunjungan = models.DateField()
    jumlah_tiket = models.IntegerField()
    class Meta:
        unique_together = ('username_p', 'nama_atraksi', 'tanggal_kunjungan')