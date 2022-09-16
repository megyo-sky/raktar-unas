from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from raktar.forms import BevetelalapForm, BeveteltermekForm
from raktar.models import Termek
from raktar.models import Raktarkeszlet
from raktar.models import Bevetel
from django.forms import formset_factory
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@staff_member_required(login_url='/login/')
def bevetel_new(request):
    TermekFormset = formset_factory(BeveteltermekForm)
    current_user = request.user
    hibas_felvitel = []
    if request.method == "POST":
        form = BevetelalapForm(request.POST)
        termekform = TermekFormset(request.POST)
        if form.is_valid() and termekform.is_valid():
            beszallito = form.cleaned_data['beszallito']
            bevetel_datum = form.cleaned_data['bevetel_datum']
            szallitolevel_szam = form.cleaned_data['szallitolevel_szam']
            megjegyzes = form.cleaned_data['megjegyzes']

            if termekform is not None:
                for item in termekform.cleaned_data:
                     try:
                        termek_nev = item['termek']
                        termek_id = item['termek_id']
                        raktar = item['raktar']
                        bevetel_mennyiseg = item['bevetel_mennyiseg']
                        ar_bevetel_netto = item['ar_bevetel_netto']
                        termek = get_object_or_404(Termek, pk=termek_id)

                        bevetelezes = Bevetel(beszallito=beszallito, bevetel_datum=bevetel_datum, szallitolevel_szam=szallitolevel_szam, megjegyzes=megjegyzes, termek=termek, raktar=raktar, bevetel_mennyiseg=bevetel_mennyiseg, ar_bevetel_netto=ar_bevetel_netto, user=current_user)
                        bevetelezes.save()

                        raktarkeszlet = Raktarkeszlet.objects.filter(termek=termek, raktar=raktar)

                        if not raktarkeszlet.count():
                            uj_raktarkeszlet = Raktarkeszlet(raktar=raktar, termek=termek, keszlet=bevetel_mennyiseg)
                            uj_raktarkeszlet.save()
                        else:
                            raktarkeszlet_id = Raktarkeszlet.objects.get(termek=termek, raktar=raktar)
                            raktarkeszlet_mennyiseg = raktarkeszlet_id.keszlet
                            uj_mennyiseg = raktarkeszlet_mennyiseg + bevetel_mennyiseg
                            raktarkeszlet_id.keszlet = uj_mennyiseg
                            raktarkeszlet_id.save()
                        messages.add_message(request, messages.SUCCESS, 'Sikeres bedolgozás')
                     except:
                        try:
                            hibas_felvitel.append(termek_nev)
                        except:
                            pass
                        messages.add_message(request, messages.ERROR(), 'Hibás bedolgozás')
            else:
                return HttpResponse('Nincs termék!', content_type="text/plain")
        else:
            hibas_felvitel.append('Nem valid form. Nem sikerült elküldeni az adatokat')
            # messages.add_message(request, messages.SUCCESS, 'Hibás felvitel')

    form = BevetelalapForm()
    termekform = TermekFormset()

    return render(
        request,
        'app/bevetelezes_new.html',
        {
            'title': 'Bevételezés',
            'form': form,
            'termekform': termekform,
            'hibas_felvitel': hibas_felvitel
        }
    )