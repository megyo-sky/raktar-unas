import datetime
import os
from raktar.models import Termek, Beallitas
from django.conf import settings
import xml.etree.ElementTree as et
import requests, csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.management.base import BaseCommand
from raktar.views.szinkron import *
from raktar.views.level import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cron_szinkron()
        level()

