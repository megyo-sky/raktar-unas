from django.db import models


class Beallitas(models.Model):
    alap_aruhaz_nev = models.CharField(max_length=255, blank=True, null=True)
    alap_aruhaz_KEY = models.CharField(max_length=255, blank=True, null=True)
    alap_aruhaz_aktiv = models.BooleanField(default=False)
    alap_aruhaz_kezdeti_arszinkron = models.BooleanField(default=False)
    alap_aruhaz_clean = models.BooleanField(default=False)
    masodik_aruhaz_nev = models.CharField(max_length=255, blank=True, null=True)
    masodik_aruhaz_KEY = models.CharField(max_length=255, blank=True, null=True)
    masodik_aruhaz_aktiv = models.BooleanField(default=False)
    masodik_aruhaz_kezdeti_arszinkron = models.BooleanField(default=False)
    masodik_aruhaz_clean = models.BooleanField(default=False)
    harmadik_aruhaz_nev = models.CharField(max_length=255, blank=True, null=True)
    harmadik_aruhaz_KEY = models.CharField(max_length=255, blank=True, null=True)
    harmadik_aruhaz_aktiv = models.BooleanField(default=False)
    harmadik_aruhaz_kezdeti_arszinkron = models.BooleanField(default=False)
    harmadik_aruhaz_clean = models.BooleanField(default=False)
    iweld_szinkron = models.BooleanField(default=False)
    iweld_api_nev = models.CharField(max_length=255, blank=True, null=True)
    iweld_api_pass = models.CharField(max_length=255, blank=True, null=True)
    Mastroweld_szinkron = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Beállítások"

    def __str__(self):
        return str(self.alap_aruhaz_nev)

