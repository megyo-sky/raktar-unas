from django.http import HttpResponse
from django.db.models import Q
from raktar.forms import Beszallito
from raktar.models import Termek, termek_riport, TermekKategoria, TermekGyarto
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
import json


# API-k
# Értékesítés termék keresés
@login_required(login_url='/login/')
def get_termek(request):
    if request.is_ajax():
        param = request.GET.get('term', None)
        termek = Termek.objects.filter(Q(termek_nev__icontains=param) | Q(gyari_cikkszam__icontains=param))[:20]
        results = []
        for t in termek:
            termek_json = {}
            termek_json['id'] = t.id
            termek_json['value'] = t.gyari_cikkszam + " -  " + t.termek_nev
            results.append(termek_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    return HttpResponse(data, 'application/json')


# Termékek lista API
@login_required(login_url='/login/')
def get_termek_api(request):
    termek_list = Termek.objects.all().values()
    termekek = json.dumps(list(termek_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return HttpResponse(termekek, 'application/json')


# Termék kategória lista API
@login_required(login_url='/login/')
def get_termekkategoria_api(request):
    termekkategoria_list = TermekKategoria.objects.all().values()
    termekkategoria = json.dumps(list(termekkategoria_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return HttpResponse(termekkategoria, 'application/json')


# Termék gyártó lista API
@login_required(login_url='/login/')
def get_termekgyarto_api(request):
    termekgyarto_list = TermekGyarto.objects.all().values()
    termekgyarto = json.dumps(list(termekgyarto_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return HttpResponse(termekgyarto, 'application/json')


class TermekAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Termek.objects.none()

        qs = Termek.objects.all()

        if self.q:
            qs = qs.filter(termek_nev__icontains=self.q)

        return qs

# Bevételezés beszállító keresés
class BeszallitoAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Beszallito.objects.none()

        qs = Beszallito.objects.all()

        if self.q:
            qs = qs.filter(beszallito_nev__icontains=self.q)

        return qs
