import os
from django.contrib.auth.decorators import login_required
from raktar.forms import DokForm
from raktar.models import Dokumentum
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from raktar.models import Termek


@login_required(login_url='/login/')
def dok_list(request, pk):
    doklist = Dokumentum.objects.filter(termek_id=pk).order_by('felt_datum').reverse()
    termek = Termek.objects.get(id=pk)
    termek_nev = termek.termek_nev

    return render(request, 'app/dok_list.html',
                  {'title': 'Dokumentumok', 'doklist': doklist, 'termeknev': termek_nev, 'termek_id': pk})


@login_required(login_url='/login/')
def dok_new(request, pk):
    if request.method == "POST":
        form = DokForm(request.POST, request.FILES)
        if form.is_valid():
            dok = form.save(commit=False)
            today = timezone.now()
            dok.felt_datum = today
            dok.termek_id = pk
            dok.save()
            return redirect('dok_list', pk=pk)
    else:
        form = DokForm()
    return render(request, 'app/dok_new.html', {'form': form})


@staff_member_required(login_url='/login/')
def dok_del(pk, termek_id):
    dok = Dokumentum.objects.get(id=pk)
    docnev = str(dok.dokfile)
    dok.delete()

    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, docnev))

    except ValueError:
        print("Valami gáz van...")

    return redirect('dok_list', pk=termek_id)
