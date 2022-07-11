from django.db import models

class Beszallito(models.Model):
    beszallito_nev = models.CharField(max_length=255, blank=False, null=False)
    beszallito_cim = models.CharField(max_length=255, blank=True, null=True)
    beszallito_ugyintezo = models.CharField(max_length=255, blank=True, null=True)
    beszallito_email = models.EmailField(blank=True, null=True)
    beszallito_telefon = models.CharField(max_length=255, blank=True, null=True)
    megjegyzes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Beszállítók"

    def __str__(self):
        return self.beszallito_nev