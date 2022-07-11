from django.db import models
from django.contrib.auth.models import User
from raktar.models import Beszallito
from raktar.models import Termek
from raktar.models import Raktar
from django.core.validators import MinValueValidator

class Bevetel(models.Model):
    beszallito = models.ForeignKey(Beszallito, blank=False, null=False, on_delete=models.RESTRICT)
    termek = models.ForeignKey(Termek, blank=False, null=False, on_delete=models.RESTRICT)
    raktar = models.ForeignKey(Raktar, blank=False, null=False, on_delete=models.RESTRICT)
    bevetel_mennyiseg = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    ar_bevetel_netto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bevetel_datum = models.DateField(blank=False, null=False)
    szallitolevel_szam = models.CharField(max_length=255, blank=True, null=True)
    megjegyzes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='user_bevetel', related_query_name="bevetelezo", on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "Bevételezés"

    def __str__(self):
        return u"%s -  %s" % (self.bevetel_datum, self.raktar)