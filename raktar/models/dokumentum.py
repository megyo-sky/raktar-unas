import datetime
import hashlib
import os
from django.db import models


def content_file_name(instance, filename):
    now = datetime.datetime.now()
    ev = str(now.year)
    ho = str(now.month)
    ext = filename.split('.')[-1]
    filename = "%s_%s" % (instance.dok_nev, now )
    md5 = hashlib.md5(filename.encode('utf-8')).hexdigest()
    filenamemd5 = "%s.%s" % (md5, ext)
    return os.path.join('documents/' + ev + '/' + ho, filenamemd5)


class Dokumentum(models.Model):
    termek_id = models.IntegerField(blank=False, null=False)
    felt_datum = models.DateField(blank=False, null=False)
    dok_nev = models.CharField(max_length=255, blank=False, null=False)
    dokfile = models.FileField(upload_to=content_file_name)

    class Meta:
        verbose_name_plural = "Dokumentumok"

    def __str__(self):
        return self.dok_nev