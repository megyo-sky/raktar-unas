from django.db import models
from raktar.models import Termek
from django.core.validators import MinValueValidator


class keszlet_riport(models.Model):
    termek_id = models.CharField(max_length=255)
    termek_nev = models.CharField(max_length=255)
    gyari_cikkszam = models.CharField(max_length=255)
    sajat_cikkszam = models.CharField(max_length=255)
    raktar_nev = models.CharField(max_length=255)
    keszlet = models.CharField(max_length=255)
    mennyisegi_egyseg = models.CharField(max_length=255)


    class Meta:
        managed = False
        db_table = 'keszlet_riport'


class termek_riport(models.Model):
    termek_nev = models.CharField(max_length=255)
    gyari_cikkszam = models.CharField(max_length=255)
    sajat_cikkszam = models.CharField(max_length=255)
    ar_web_netto = models.CharField(max_length=255)
    ar_bolt_brutto = models.CharField(max_length=255)
    elhelyezes = models.CharField(max_length=255)
    min_keszlet = models.CharField(max_length=255)
    mennyisegi_egyseg = models.CharField(max_length=255)
    web_link = models.CharField(max_length=255)
    termekkategoria = models.CharField(max_length=255)
    termekgyarto = models.CharField(max_length=255)
    megjegyzes = models.CharField(max_length=255)
    aktiv = models.BooleanField()


    class Meta:
        managed = False
        db_table = 'termek_riport'


class bevetel_riport(models.Model):
    termek_id = models.CharField(max_length=255)
    termek_nev = models.CharField(max_length=255)
    gyari_cikkszam = models.CharField(max_length=255)
    sajat_cikkszam = models.CharField(max_length=255)
    beszallito_nev = models.CharField(max_length=255)
    raktar_nev = models.CharField(max_length=255)
    bevetel_mennyiseg = models.CharField(max_length=255)
    ar_bevetel_netto = models.CharField(max_length=255)
    bevetel_datum = models.CharField(max_length=255)
    szallitolevel_szam = models.CharField(max_length=255)
    megjegyzes = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    azonosito = models.CharField(max_length=255)


    class Meta:
        managed = False
        db_table = 'bevetel_riport'


class ertekesit_riport(models.Model):
    termek_id = models.CharField(max_length=255)
    azonosito = models.CharField(max_length=255)
    termek_nev = models.CharField(max_length=255)
    gyari_cikkszam = models.CharField(max_length=255)
    sajat_cikkszam = models.CharField(max_length=255)
    raktar_nev = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    megjegyzes = models.CharField(max_length=255)
    eladas_mennyiseg = models.CharField(max_length=255)
    ar_eladas_brutto = models.CharField(max_length=255)
    eladas_datum = models.CharField(max_length=255)


    class Meta:
        managed = False
        db_table = 'ertekesit_riport'