from django.db import models

# Create your models here.

class CatatanMedis(models.Model):
    id_hewan = models.ForeignKey('Hewan', on_delete=models.CASCADE)
    username_dh = models.ForeignKey('Dokter_Hewan', on_delete=models.CASCADE)
    tanggal_pemeriksaan = models.DateField()
    diagnosis = models.CharField(max_length=100, blank=True, null=True)
    pengobatan = models.CharField(max_length=100, blank=True, null=True)
    status_kesehatan = models.CharField(max_length=50)
    catatan_tindak_lanjut = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('id_hewan', 'tanggal_pemeriksaan')
        ordering = ['-tanggal_pemeriksaan']

    def __str__(self):
        return f"{self.id_hewan} - {self.tanggal_pemeriksaan}"
