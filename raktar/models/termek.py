from django.db import models
from django.core.validators import URLValidator
from django.core.validators import MinValueValidator


class TermekGyarto(models.Model):
    termekgyarto = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = "Termék gyártók"
        ordering = ('termekgyarto',)

    def __str__(self):
        return self.termekgyarto

class TermekKategoria(models.Model):
    termekkategoria = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = "Termék kategóriák"
        ordering = ('termekkategoria',)

    def __str__(self):
        return self.termekkategoria


class Termek(models.Model):
    MENNYISEGI_EGYSEG = (
        ('', 'Kérem válasszon'),
        ('csomag', 'csomag'),
        ('db', 'db'),
        ('kg', 'kilogramm'),
        ('méter', 'Méter'),
    )
    termek_nev = models.CharField(max_length=255, blank=False, null=False)
    gyari_cikkszam = models.CharField(max_length=255, blank=False, null=False, db_index=True,)
    sajat_cikkszam = models.CharField(max_length=255, blank=True, null=True, db_index=True,)
    ar_nagyker_netto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    alap_bolt_ar_brutto = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    masodik_bolt_ar_brutto = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    harmadik_bolt_ar_brutto = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    elhelyezes = models.CharField(max_length=255, blank=True, null=True)
    min_keszlet = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False, default=0)
    mennyisegi_egyseg = models.CharField(max_length=255, choices=MENNYISEGI_EGYSEG, blank=False, null=False)
    web_link = models.TextField(validators=[URLValidator()], blank=True, null=True)
    termekkategoria = models.ForeignKey(TermekKategoria, blank=True, null=True, on_delete=models.RESTRICT)
    termekgyarto = models.ForeignKey(TermekGyarto, blank=True, null=True, on_delete=models.RESTRICT)
    megjegyzes = models.TextField(blank=True, null=True)
    nagyker_keszlet = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    alap_aruhaz = models.BooleanField(default=False)
    masodik_aruhaz = models.BooleanField(default=False)
    harmadik_aruhaz = models.BooleanField(default=False)

    aktiv = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Termékek"
        unique_together = ('gyari_cikkszam', 'termek_nev')

    def __str__(self):
        return str(self.termek_nev)

