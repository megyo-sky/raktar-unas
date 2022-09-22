import datetime
import os
from raktar.models import Termek, Beallitas
from django.conf import settings
import xml.etree.ElementTree as et
import requests, csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        set = Beallitas.objects.get(id=1)

        # if set.iweld_szinkron:
        #     nev = set.iweld_api_nev
        #     pas = set.iweld_api_pass
        #     iweld_stock_nagyker_szinkron(nev, pas)

        if set.Mastroweld_szinkron:
            print("elindul")
            mas_nagyker_szinkron()
        print(" nem elindul")

