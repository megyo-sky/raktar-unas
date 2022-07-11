from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from raktar.forms import TermekSearchForm
from raktar.models import Termek, Termek_Osszdb
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def index(request):
    if request.method == "POST":
        form = TermekSearchForm(request.POST)
        if form.is_valid():
            param = form.cleaned_data['autocomplete']
            param_id = form.cleaned_data['autocomplete_id']

            if param_id == None:
                termekek = Termek.objects.filter(Q(termek_nev__icontains=param) | Q(gyari_cikkszam__icontains=param) | Q(sajat_cikkszam__icontains=param))[:200]
                return render(request, 'app/index.html', {'title': 'Értékesítés termék lista', 'termekek': termekek, 'form': form, 'data': True})

            if param_id != None:
                return redirect('termek_ertekesites', pk=param_id)

    else:
        form = TermekSearchForm()

    return render(
        request,
        'app/index.html',
        {
            'title': 'Értékesítés termék kereső',
            'form': form,
            'data': False
        }
    )


def email_termek_osszdb(request):
    raktar_keszlet = Termek_Osszdb.objects.all()
    email_kuld = False
    email_szoveg = "Kedves Péter!\n\nA következő termékeknek csökkent a készlete a megadott minimum alá: \n\n"

    for k in raktar_keszlet:
        min_keszlet = k.min_keszlet
        akt_keszlet = k.keszlet
        if akt_keszlet < min_keszlet:
            email_kuld = True
            email_szoveg += "Termék neve: " + k.termek_nev + " -- Gyári cikkszáma: " + k.gyari_cikkszam + " -- Jelenlegi készlet: " + str(k.keszlet) + "\n"

    if email_kuld:
        pass
        # send_mail(
        #     'Raktárkészlet figyelés',
        #     email_szoveg,
        #     'info@hegesztescentrum.hu',
        #     ['medgyesi.peter@gmail.com'],
        #     fail_silently=False,
        # )

    return HttpResponse(email_szoveg, content_type="text/plain")
