from django.contrib.auth.models import User
from django.db import models
from raktar.models import Termek


class Raktar(models.Model):
    raktar_nev = models.CharField(max_length=255, blank=False, null=False, unique=True)
    megjegyzes = models.TextField(blank=True, null=True)
    user = models.ManyToManyField(User, related_name='user_raktar', related_query_name="raktarjog")

    class Meta:
        verbose_name_plural = "Raktárak"
        ordering = ('raktar_nev',)

    def __str__(self):
        return self.raktar_nev


class Raktarkeszlet(models.Model):
    termek = models.ForeignKey(Termek, blank=False, null=False, on_delete=models.RESTRICT)
    raktar = models.ForeignKey(Raktar, blank=False, null=False, on_delete=models.RESTRICT)
    keszlet = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Raktárkészlet"
        unique_together = ('termek', 'raktar')

    def __str__(self):
        return str(self.termek) #+ "   " + str(self.keszlet)


class Termek_Osszdb(models.Model):
    termek_id = models.CharField(max_length=255, primary_key=True)
    termek_nev = models.CharField(max_length=255)
    sajat_cikkszam = models.CharField(max_length=255)
    gyari_cikkszam = models.CharField(max_length=255)
    # min_keszlet = models.CharField(max_length=255)
    # keszlet = models.CharField(max_length=255)
    min_keszlet = models.DecimalField(max_digits=10, decimal_places=2)
    keszlet = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'termek_osszdb'