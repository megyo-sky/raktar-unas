import os
import csv
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from raktar.forms import ErtekesitForm
from raktar.forms import TermekForm
from raktar.forms import TermekImport, ArImport
from raktar.forms import TermekAtvazetAlapForm
from raktar.forms import TermekAtvezetTermekForm
from raktar.models import TermekKategoria, TermekGyarto
from raktar.models import Termek, Raktarkeszlet, Bevetel, Beallitas
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@login_required(login_url='/login/')
def termek_list(request):
    # termek_list = termek_riport.objects.all().values()
    # termekek = json.dumps(list(termek_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/termek_list.html',
        {
            'title': 'Termékek listája',
            # 'termekek': termekek,
        }
    )


@staff_member_required(login_url='/login/')
def termek_new(request):
    if request.method == "POST":
        form = TermekForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('termek_list')
    else:
        form = TermekForm()

    return render(
        request,
        'app/termek_new.html',
        {
            'title': 'Új termék létrehozása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termek_edit(request, pk):
    termek = get_object_or_404(Termek, pk=pk)
    if request.method == "POST":
        form = TermekForm(request.POST, instance=termek)
        if form.is_valid():
            form.save()
            return redirect('termek_list')
    else:
        form = TermekForm(instance=termek)

    return render(
        request,
        'app/termek_edit.html',
        {
            'title': 'Termék módosítása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termek_atvezetes(request):
    TermekFormset = formset_factory(TermekAtvezetTermekForm)
    hibas_felvitel = []

    if request.method == "POST":
        form = TermekAtvazetAlapForm(request.POST)
        termekform = TermekFormset(request.POST)

        if form.is_valid() and termekform.is_valid():
            raktarbol = form.cleaned_data['raktarbol']
            raktarba = form.cleaned_data['raktarba']

            if raktarbol == raktarba:
                hibas_felvitel.append("Egyező raktárak!")

            if termekform is not None and raktarbol != raktarba:
                for item in termekform.cleaned_data:
                     try:
                        termek_nev = item['termek']
                        termek_id = item['termek_id']
                        mennyiseg = item['mennyiseg']
                        termek = get_object_or_404(Termek, pk=termek_id)

                        raktarkeszletbol = Raktarkeszlet.objects.get(termek=termek, raktar=raktarbol)
                        jelenlegi_mennyiseg_bol = raktarkeszletbol.keszlet

                        # Ha nincs még bevételezés a cél raktárba
                        try:
                            raktarkeszletbe = Raktarkeszlet.objects.get(termek=termek, raktar=raktarba)
                            jelenlegi_mennyiseg_be = raktarkeszletbe.keszlet
                        except:
                            bevetelezes = Raktarkeszlet(termek=termek, raktar=raktarba, keszlet=0)
                            bevetelezes.save()
                            raktarkeszletbe = Raktarkeszlet.objects.get(termek=termek, raktar=raktarba)
                            jelenlegi_mennyiseg_be = raktarkeszletbe.keszlet

                        # Ha a átvezetendő mennyiség nagyobb mint a készlet akkor hibalista
                        if mennyiseg > jelenlegi_mennyiseg_bol:
                            hibas_felvitel.append(termek_nev + " -- " + str(jelenlegi_mennyiseg_bol) + "-bol " + str(mennyiseg) + " -t szeretett volna átvezetni.")
                        else:
                            aktualis_mennyiseg_bol = jelenlegi_mennyiseg_bol - mennyiseg
                            raktarkeszletbol.keszlet = aktualis_mennyiseg_bol
                            raktarkeszletbol.save()

                            aktualis_mennyiseg_be = mennyiseg + jelenlegi_mennyiseg_be
                            raktarkeszletbe.keszlet = aktualis_mennyiseg_be
                            raktarkeszletbe.save()

                     except:
                        try:
                            hibas_felvitel.append(termek_nev + " -  Nem átvezethető")
                        except:
                            pass
            else:
                pass #return HttpResponse('Nincs termék!', content_type="text/plain")
            # return redirect('termek_atvezetes')
    # else:
    form = TermekAtvazetAlapForm()
    termekform = TermekFormset()

    return render(
        request,
        'app/termek_atvezetes.html',
        {
            'title': 'Termék átvezetés',
            'form': form,
            'termekform': termekform,
            'hibas_felvitel': hibas_felvitel
        }
    )


@staff_member_required(login_url='/login/')
def termek_import(request):
    hiba_import = []
    with open(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'), 'r', encoding='utf-8') as termek_import:
        reader = csv.reader(termek_import, delimiter=';')
        next(reader)
        for index, row in enumerate(reader):
            try:
                termek_nev = row[0].strip()
                gyari_cikkszam = row[1].strip()
                # sajat_cikkszam = row[2].strip()
                ar_nagyker_netto = float(row[2].strip())
                alap_bolt_ar_brutto = int(row[3].strip())
                elhelyezes = row[4].strip()
                min_keszlet = int(row[5].strip())
                mennyisegi_egyseg = row[6].strip()
                termekkat = row[7].strip()
                if termekkat == '':
                    termekkat = 0
                else:
                    termekkat = int(row[7].strip())

                termek_gyarto = row[8].strip()
                if termek_gyarto == '':
                    termek_gyarto = 0
                else:
                    termek_gyarto = row[8].strip()

                aktiv = row[9].strip()
                megjegyzes = row[10].strip()
                web_link = row[11].strip()

                try:
                    termekkategoria = TermekKategoria.objects.get(pk=termekkat)
                except:
                    termekkategoria = None

                try:
                    termekgyarto = TermekGyarto.objects.get(pk=termek_gyarto)
                except:
                    termekgyarto = None

                termek = Termek(termek_nev=termek_nev, gyari_cikkszam=gyari_cikkszam, ar_nagyker_netto=ar_nagyker_netto,
                                alap_bolt_ar_brutto=alap_bolt_ar_brutto, elhelyezes=elhelyezes, min_keszlet=min_keszlet, mennyisegi_egyseg=mennyisegi_egyseg,
                                web_link=web_link, termekkategoria=termekkategoria, megjegyzes=megjegyzes, aktiv=aktiv, termekgyarto=termekgyarto)
                termek.save()
            except Exception as e:
                h = str(index+1) + " - " + termek_nev + " - " + str(e)
                hiba_import.append(h)

    # Hibára futott import termékek file-ba írása
    with open(os.path.join(settings.MEDIA_ROOT, 'export/termek_import_error.csv'), 'w', encoding='utf-8') as termek_import_error:
        termek_import_error.write('\n'.join(hiba_import))

    # ha van hiba akkor paraméterrel átirányít
    if not hiba_import:
        return redirect('termek_import_feltolt')
    else:
        return redirect(reverse('termek_import_feltolt') + '?hiba=1')


@staff_member_required(login_url='/login/')
def termek_import_feltolt(request):
    form = TermekImport()
    termek_lista = []
    hiba_import = ""
    termek_import_hiba = False
    set = Beallitas.objects.get(id=1)

    # Importálandó termékek file törlése
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv')):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'))

    # Ha létezik a termék imoprt hiba paraméter akkor a nézetben megjelenítjük a hibafile linket
    if request.method == 'GET' and 'hiba' in request.GET:
        hiba = request.GET['hiba']

        if hiba == '1':
            termek_import_hiba = True

    if request.method == "POST" and request.FILES['termekek']:
        # Nem importált termékek file törlése
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/termek_import_error.csv')):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'export/termek_import_error.csv'))
            termek_import_hiba = False

        # Termék import file létrehozása
        myfile = request.FILES['termekek']
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(settings.MEDIA_ROOT,'export/termek_import.csv'), myfile)
        # uploaded_file_url = fs.url(filename)

        # Ha sikerült megnyitni a termék import file-t akkor beolvasom, ha nem törlöm az import file-t és error log létrehozás
        try:
            with open(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'), 'r', encoding='utf-8') as termek_import:
                sorok = csv.reader(termek_import, delimiter=';',)
                next(sorok)
                termek_lista = list(sorok)
        except:
            today = timezone.now()
            with open(os.path.join(settings.MEDIA_ROOT, 'export/error_log.csv'), 'a+', encoding='utf-8') as error_log:
                error_log.write(str(today) + " -  File betöltés valami nem volt jó! \n")
                hiba_import = "Hibás a betöltött fájl!"
                termek_lista = []

                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv')):
                    os.remove(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'))

    return render(request, 'app/termek_import.html', {'form': form, 'title': 'Termék import', 'termek_lista': termek_lista, 'hiba_import': hiba_import, 'termek_hiba': termek_import_hiba, 'set': set})


@staff_member_required(login_url='/login/')
def ar_import(request):
    hiba_import = []
    with open(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv'), 'r', encoding='utf-8') as ar_import:
        reader = csv.reader(ar_import, delimiter=';')
        next(reader)
        for index, row in enumerate(reader):
            try:
                cikkszam = row[0].strip()
                elso_ar = row[1].strip()
                if elso_ar == '':
                    elso_ar = False
                else:
                    elso_ar = int(float(elso_ar.replace(',', '.')))

                masodik_ar = row[2].strip()
                if masodik_ar == '':
                    masodik_ar = False
                else:
                    masodik_ar = int(float(masodik_ar.replace(',', '.')))

                harmadik_ar = row[3].strip()
                if harmadik_ar == '':
                    harmadik_ar = False
                else:
                    harmadik_ar = int(float(harmadik_ar.replace(',', '.')))

                if Termek.objects.filter(gyari_cikkszam=cikkszam).exists():
                    if elso_ar:
                        Termek.objects.filter(gyari_cikkszam=cikkszam).update(alap_bolt_ar_brutto=elso_ar)
                        print("Mod 1")
                    if masodik_ar:
                        Termek.objects.filter(gyari_cikkszam=cikkszam).update(masodik_bolt_ar_brutto=masodik_ar)
                        print("Mod 2")
                    if harmadik_ar:
                        Termek.objects.filter(gyari_cikkszam=cikkszam).update(harmadik_bolt_ar_brutto=harmadik_ar)
                        print("Mod 3")
            except Exception as e:
                h = str(index+1) + " - " + cikkszam + " - " + str(e)
                hiba_import.append(h)

    # Hibára futott import termékek file-ba írása
    with open(os.path.join(settings.MEDIA_ROOT, 'export/ar_import_error.csv'), 'w', encoding='utf-8') as ar_import_error:
        ar_import_error.write('\n'.join(hiba_import))

    # ha van hiba akkor paraméterrel átirányít
    if not hiba_import:
        return redirect('ar_import_feltolt')
    else:
        return redirect(reverse('ar_import_feltolt') + '?hiba=1')



@staff_member_required(login_url='/login/')
def ar_import_feltolt(request):
    form = ArImport()
    ar_lista = []
    hiba_import = ""
    ar_import_hiba = False
    set = Beallitas.objects.get(id=1)

    # Importálandó termékek file törlése
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv')):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv'))

    # Ha létezik a termék imoprt hiba paraméter akkor a nézetben megjelenítjük a hibafile linket
    if request.method == 'GET' and 'hiba' in request.GET:
        hiba = request.GET['hiba']

        if hiba == '1':
            ar_import_hiba = True

    if request.method == "POST" and request.FILES['ar']:
        # Nem importált termékek file törlése
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/ar_import_error.csv')):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'export/ar_import_error.csv'))
            ar_import_hiba = False

        # Termék import file létrehozása
        myfile = request.FILES['ar']
        # name, ext = os.path.splitext(myfile.name)
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(settings.MEDIA_ROOT,'export/ar_import.csv'), myfile)
        # uploaded_file_url = fs.url(filename)

        # Ha sikerült megnyitni a termék import file-t akkor beolvasom, ha nem törlöm az import file-t és error log létrehozás
        try:
            with open(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv'), 'r', encoding='utf-8') as ar_import:
                sorok = csv.reader(ar_import, delimiter=';',)
                next(sorok)
                ar_lista = list(sorok)
        except:
            today = timezone.now()
            with open(os.path.join(settings.MEDIA_ROOT, 'export/error_log.csv'), 'a+', encoding='utf-8') as error_log:
                error_log.write(str(today) + " -  File betöltés hiba! \n")
                hiba_import = "Hibás a betöltött fájl!"
                ar_lista = []

                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv')):
                    os.remove(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv'))

    return render(request, 'app/ar_import.html', {'form': form, 'title': 'Ár import', 'ar_lista': ar_lista, 'hiba_import': hiba_import, 'ar_hiba': ar_import_hiba, 'set': set})


@login_required(login_url='/login/')
def termek_ertekesites(request, pk):
    termek = get_object_or_404(Termek, pk=pk)
    raktarkeszlet = Raktarkeszlet.objects.filter(termek=pk)
    set = Beallitas.objects.get(id=1)
    # alap_aruhaz_nev = set.alap_aruhaz_nev
    # masodik_aruhaz_nev = set.masodik_aruhaz_nev
    # harmadik_aruhaz_nev = set.harmadik_aruhaz_nev
    last_bevetel_ar = 0
    try:
        last_bevetel_ar = Bevetel.objects.filter(termek=pk).order_by('-id')[0]
    except:
        pass
    current_user = request.user

    if request.method == "POST":
        form = ErtekesitForm(current_user, request.POST)
        if form.is_valid():
            ertekesit = form.save(commit=False)
            ertekesit.termek = termek
            today = timezone.now()
            ertekesit.eladas_datum = today
            ertekesit.user = current_user
            ertekesit.save()

            #    Készlet módosítása
            try:
                keszlet_id = Raktarkeszlet.objects.get(termek=pk, raktar=ertekesit.raktar)
                raktárkeszlet = keszlet_id.keszlet
                uj_keszlet = raktárkeszlet - ertekesit.eladas_mennyiseg

                # mehet mínuszba is
                # if uj_keszlet <= 0:
                #     uj_keszlet = 0

                keszlet_id.keszlet = uj_keszlet
                keszlet_id.save()
            except:
                pass

            return redirect('index')
    else:
        form = ErtekesitForm(current_user)

    # return HttpResponse(raki, content_type="text/plain")
    return render(request, 'app/termek_ertekesites.html', {'title': 'Értékesítés termék', 'termek': termek, 'raktarkeszlet': raktarkeszlet, 'last_bevetel_ar':last_bevetel_ar, 'set':set, 'form': form})
