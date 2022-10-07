import datetime
import os
from raktar.models import Termek, Beallitas, Raktarkeszlet, Ertekesit, Raktar
from django.conf import settings
import xml.etree.ElementTree as et
import requests, csv
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from decimal import Decimal


def adderrorlist(error):
    global errorlist
    errorlist = True
    date = datetime.datetime.now()
    with open(os.path.join(settings.MEDIA_ROOT, 'error.log'), 'a') as f:
        f.write(str(date) + " - " + error + "\n")
    print("Hiba: " + error)
#
# get magento admin token
def getUnasToken(aruhaz):
    set = Beallitas.objects.get(id=1)
    if aruhaz == 'alap_aruhaz':
        key= set.alap_aruhaz_KEY
    elif aruhaz == 'masodik_aruhaz':
        key= set.masodik_aruhaz_KEY
    elif aruhaz == 'harmadik_aruhaz':
        key= set.harmadik_aruhaz_KEY
    else:
        key= "0"
        adderrorlist('Nincs áruház azonosító')

    urlToken = 'https://api.unas.eu/shop/login'
    auth = '''<Params><ApiKey>'''+key+'''</ApiKey></Params>'''
    headers = {'Content-Type': 'text/xml'}
    responseToken = requests.get(urlToken, data=auth, headers=headers)
    t = responseToken.text
    root = et.fromstring(t)
    # print(root)
    if root.tag =='Error':
        adderrorlist(root.text)
        print(root.tag)
        return False
    else:
        for child in root.findall('Token'):
            token = child.text
            print("Login token: " + token)
            return token


def unas_download(aruhaz, token):
    urlToken = 'https://api.unas.eu/shop/getProduct'
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'text/xml'}
    param = '''<Params><ContentType>short</ContentType></Params>'''
    response = requests.get(urlToken, data=param, headers=headers)
    if response.status_code == requests.codes.ok:
        products = response.text
        with open(os.path.join(settings.MEDIA_ROOT, 'import/'+aruhaz+'_termek_import.xml'), 'w', encoding='utf-8') as f:
            f.write(products)
    print("Letöltés kész: " + aruhaz)


def dataclean(aruhaz):
    set = Beallitas.objects.get(id=1)

    if aruhaz == "alap_aruhaz":
        if set.alap_aruhaz_clean:
            Termek.objects.update(alap_aruhaz=0, alap_bolt_ar_brutto=0)
        else:
            Termek.objects.update(alap_aruhaz=0)
        Beallitas.objects.filter(id=1).update(alap_aruhaz_clean=0)

    elif aruhaz == "masodik_aruhaz":
        if set.masodik_aruhaz_clean:
            Termek.objects.update(masodik_aruhaz=0, masodik_bolt_ar_brutto=0)
        else:
            Termek.objects.update(masodik_aruhaz=0)
        Beallitas.objects.filter(id=1).update(masodik_aruhaz_clean=0)

    elif aruhaz == "harmadik_aruhaz":
        if set.harmadik_aruhaz_clean:
            Termek.objects.update(harmadik_aruhaz=0, harmadik_bolt_ar_brutto=0)
        else:
            Termek.objects.update(harmadik_aruhaz=0)
        Beallitas.objects.filter(id=1).update(harmadik_aruhaz_clean=0)

    print("Dataclean kész " + aruhaz)


def unas_betolto(aruhaz):
    set = Beallitas.objects.get(id=1)
    try:
        xml = str(os.path.join(settings.MEDIA_ROOT) + '/import/'+aruhaz+'_termek_import.xml')
        tree = et.parse(xml)
        root = tree.getroot()
        dataclean(aruhaz)
        # print(root.tag)
        list=[]
        for child in root:
            state = (child.find('State').text)
            if state != 'deleted':
                cikkszam = (child.find('Sku').text)
                name = (child.find('Name').text)
                egyseg = (child.find('Unit').text)
                price = int(float(child.find('Prices')[1].find('Gross').text))

                if Termek.objects.filter(gyari_cikkszam=cikkszam).exists():
                    if aruhaz == "alap_aruhaz":
                        if set.alap_aruhaz_kezdeti_arszinkron:
                            Termek.objects.filter(gyari_cikkszam=cikkszam).update(alap_aruhaz=True, alap_bolt_ar_brutto=price)
                        else:
                            Termek.objects.filter(gyari_cikkszam=cikkszam).update(alap_aruhaz=True)

                    elif aruhaz == "masodik_aruhaz":
                        if set.masodik_aruhaz_kezdeti_arszinkron:
                            Termek.objects.filter(gyari_cikkszam=cikkszam).update(masodik_aruhaz=True, masodik_bolt_ar_brutto=price)
                        else:
                            Termek.objects.filter(gyari_cikkszam=cikkszam).update(masodik_aruhaz=True)

                    elif aruhaz == "harmadik_aruhaz":
                        if set.harmadik_aruhaz_kezdeti_arszinkron:
                            Termek.objects.filter(gyari_cikkszam=cikkszam).update(harmadik_aruhaz=True, harmadik_bolt_ar_brutto=price)
                        else:
                            Termek.objects.filter(gyari_cikkszam=cikkszam).update(harmadik_aruhaz=True)

                else:
                    if aruhaz == "alap_aruhaz":
                        list.append(Termek(gyari_cikkszam=cikkszam, termek_nev=name, alap_bolt_ar_brutto=price,mennyisegi_egyseg=egyseg, alap_aruhaz=True),)
                    elif aruhaz == "masodik_aruhaz":
                        list.append(Termek(gyari_cikkszam=cikkszam, termek_nev=name, masodik_bolt_ar_brutto=price, mennyisegi_egyseg=egyseg, masodik_aruhaz=True),)
                    elif aruhaz == "harmadik_aruhaz":
                        list.append(
                            Termek(gyari_cikkszam=cikkszam, termek_nev=name, harmadik_bolt_ar_brutto=price, mennyisegi_egyseg=egyseg, harmadik_aruhaz=True),)

        # try:
        Termek.objects.bulk_create(list)

        if aruhaz == 'alap_aruhaz':
            Beallitas.objects.filter(id=1).update(alap_aruhaz_kezdeti_arszinkron=0)
        elif aruhaz == 'masodik_aruhaz':
            Beallitas.objects.filter(id=1).update(masodik_aruhaz_kezdeti_arszinkron=0)
        elif aruhaz == 'harmadik_aruhaz':
            Beallitas.objects.filter(id=1).update(harmadik_aruhaz_kezdeti_arszinkron=0)

        # except:
        #     adderrorlist('Hiba az új termék bedolgozásnál.')

        print('Betöltés kész: ' + aruhaz)
    except:
        print('Betöltés hiba: ' + aruhaz)
        adderrorlist('Unas termék betöltés hiba')

    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'import/' + aruhaz + '_termek_import.xml')):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'import/' + aruhaz + '_termek_import.xml'))


# def unas_price_update(aruhaz, token):
#     urlToken = 'https://api.unas.eu/shop/setProduct'
#     headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'text/xml'}
#     param = '<Products>'
#
#     if aruhaz == "alap_aruhaz":
#         termekek = Termek.objects.filter(alap_aruhaz=True).values_list('gyari_cikkszam', 'alap_bolt_ar_brutto')
#     elif aruhaz == "masodik_aruhaz":
#         termekek = Termek.objects.filter(masodik_aruhaz=True).values_list('gyari_cikkszam', 'masodik_bolt_ar_brutto')
#     elif aruhaz == "harmadik_aruhaz":
#         termekek = Termek.objects.filter(harmadik_aruhaz=True).values_list('gyari_cikkszam', 'harmadik_bolt_ar_brutto')
#     for row in termekek:
#         sku = row[0]
#         price = row[1]
#         if (price != 0) and (price is not None):
#             price = str(row[1])
#             param += '<Product><Action>modify</Action><Sku>'+sku+'</Sku><Prices><Price><Type>normal</Type><Net>'+price+'</Net><Gross>'+price+'</Gross></Price></Prices></Product>'
#     param += '</Products>'
#     print(param)
#     response = requests.get(urlToken, data=param, headers=headers)
#     if response.status_code == requests.codes.ok:
#          print(response.text)
#     else:
#         print(response.text)
#
#     print("Ár módosítás kész: " + aruhaz)


def mas_nagyker_szinkron():
    url = 'https://www.mastroweld.hu/files/csv_export/sajat.csv'
    data = requests.get(url)
    data.encoding = 'utf-8'
    lines = data.text.splitlines()
    reader = csv.reader(lines, delimiter=';')
    print(" Sikeres Mas készlet letöltés")
    # with open(os.path.join(settings.MEDIA_ROOT, 'export/sajat.csv'), 'r', encoding='utf-8') as termek_import:
    #     reader = csv.reader(termek_import, delimiter=';')
    #     next(reader)

    for index, row in enumerate(reader):
        sku = row[0].strip()
        keszlet = row[5].strip()
        netto_ar = row[7].strip()
        akcios_ar = row[8].strip()
        nagyker_ar = 0

        if akcios_ar != '' and akcios_ar != 0:
            nagyker_ar = akcios_ar
        elif netto_ar != '' and netto_ar != 0:
            nagyker_ar = netto_ar

        try:
            termek = Termek.objects.get(gyari_cikkszam=sku, sajat_cikkszam='mas')
            try:
                termek.ar_nagyker_netto=nagyker_ar
                termek.nagyker_keszlet=keszlet
                termek.save()
            except Exception as ex:
                print(ex)
                adderrorlist(str(sku) + ' - Mastroweld készlet szinkron hiba')
        except:
            pass
        # print(" sku: " + sku + " --- keszlet: " + keszlet + " ---ar: " + netto_ar)


def iweld_stock_nagyker_szinkron(nev, pas):
    url = 'https://sync.vectorcloud.hu:5432/szinkron/getdata?resourceName=VA_stock&full=1'
    response = requests.get(url, auth=(nev, pas))

    if response.status_code == requests.codes.ok:
        # decoded_response = response.content.decode('utf-8')
        xml_content = response.content
        root = et.fromstring(xml_content)
        print(" Sikeres Iweld készlet letöltés")

        for child in root:
            # print(child.tag, child.attrib, child.attrib ,child.text)
            # et.dump(child)
            sku = child.find('PRODUCT_ID').text
            keszlet = int(float(child.find('STOCK').text))
            try:
                termek = Termek.objects.get(gyari_cikkszam=sku, sajat_cikkszam='iwe')
                try:
                    termek.nagyker_keszlet=keszlet
                    termek.save()
                except Exception as ex:
                    print(ex)
                    adderrorlist(str(sku)+' - Iweld készlet szinkron hiba')
            except:
                pass


def keszlet_to_unas(aruhaz):
    if aruhaz == "alap_aruhaz":
        termekek = Termek.objects.filter(alap_aruhaz=1).exclude(sajat_cikkszam=0).exclude(sajat_cikkszam__isnull=True)
    elif aruhaz == 'masodik_aruhaz':
        termekek = Termek.objects.filter(masodik_aruhaz=1).exclude(sajat_cikkszam=0).exclude(sajat_cikkszam__isnull=True)
    elif aruhaz == 'harmadik_aruhaz':
        termekek = Termek.objects.filter(harmadik_aruhaz=1).exclude(sajat_cikkszam=0).exclude(sajat_cikkszam__isnull=True)

    raktarkeszlet = Raktarkeszlet.objects.values_list('termek', flat=True)
    keszlet = set(raktarkeszlet)
    list = ['"Cikkszám";"Paraméter: Szállítás||text|1|0|1|0|0|0|||0|1|1"']

    for termek in termekek:
        if termek.nagyker_keszlet > 0:
            list.append(termek.gyari_cikkszam + '; "Raktáron, szállítás 1-2 munkanap"')
        elif termek.id in keszlet:
            list.append(termek.gyari_cikkszam + '; "Raktáron, szállítás 1-2 munkanap"')
        else:
            list.append(termek.gyari_cikkszam + '; "Rendelésre"')

    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'import/' + aruhaz + '_keszlet_to_unas.csv')):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'import/' + aruhaz + '_keszlet_to_unas.csv'))

    with open(os.path.join(settings.MEDIA_ROOT, 'import/'+aruhaz+'_keszlet_to_unas.csv'), 'w', encoding='utf-8') as f:
        for item in list:
            f.write("%s\n" % item)
    print(aruhaz+ " Sikeres keszlet_to_unas")


def unas_orders(aruhaz, token):
    raktar = get_object_or_404(Raktar, id=1)
    user = get_object_or_404(User, id=1)
    stamp = datetime.datetime.now() - datetime.timedelta(days=4)
    stamp = int(stamp.timestamp())
    # print(stamp)

    urlToken = 'https://api.unas.eu/shop/getOrder'
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'text/xml'}
    param = '<Params><Status>close_ok</Status><TimeModStart>'+str(stamp)+'</TimeModStart></Params>'
    response = requests.get(urlToken, data=param, headers=headers)
    if response.status_code == requests.codes.ok:
        # orders = response.text
        xml_content = response.content
        root = et.fromstring(xml_content)

        for child in root:
            try:
                key = child.find('Key').text
                datum = child.find('Date').text[:10]
                datum = datum.replace(".","-")
                # print(key)
                items = child.find('Items')

                ertekesit = Ertekesit.objects.filter(unas_order_key=key)
                if not ertekesit.count():
                    for item in items:
                        sku = item.find('Sku').text
                        mennyiseg = Decimal(item.find('Quantity').text)
                        ar = int(float(item.find('PriceNet').text))

                        if sku !='shipping-cost':
                            try:
                                termek = Termek.objects.get(gyari_cikkszam=sku)
                                ertekesit = Ertekesit(termek=termek, raktar=raktar, eladas_mennyiseg=mennyiseg, eladas_datum=datum,
                                                      megjegyzes=key, ar_eladas_brutto=ar, user=user, unas_order_key=key)
                                ertekesit.save()
                            except:
                                adderrorlist(str(sku) + ' - Unas eladás betöltés hiba')
                            try:
                                raktarkeszlet = Raktarkeszlet.objects.filter(termek=termek, raktar=raktar)
                                if not raktarkeszlet.count():
                                    mennyiseg = 0-mennyiseg
                                    uj_raktarkeszlet = Raktarkeszlet(raktar=raktar, termek=termek, keszlet=mennyiseg)
                                    uj_raktarkeszlet.save()
                                else:
                                    raktarkeszlet_id = Raktarkeszlet.objects.get(termek=termek, raktar=raktar)
                                    keszlet = raktarkeszlet_id.keszlet
                                    uj_keszlet = keszlet - mennyiseg

                                    raktarkeszlet_id.keszlet = uj_keszlet
                                    raktarkeszlet_id.save()
                            except:
                                adderrorlist(str(sku) + ' - Unas készlet frissítés hiba')
            except:
                adderrorlist(str(sku)+' - Unas eladás frissítés hiba')
    print("Orders kész: " + aruhaz)


def szinkron(request):
    set = Beallitas.objects.get(id=1)

    if set.alap_aruhaz_aktiv:
        token = getUnasToken('alap_aruhaz')
        unas_download('alap_aruhaz', token)
        unas_betolto('alap_aruhaz')
        unas_orders('alap_aruhaz', token)

    if set.masodik_aruhaz_aktiv:
        token = getUnasToken('masodik_aruhaz')
        unas_download('masodik_aruhaz', token)
        unas_betolto('masodik_aruhaz')
        unas_orders('masodik_aruhaz', token)

    if set.harmadik_aruhaz_aktiv:
        token = getUnasToken('harmadik_aruhaz')
        unas_download('harmadik_aruhaz', token)
        unas_betolto('harmadik_aruhaz')
        unas_orders('harmadik_aruhaz', token)
        # unas_price_update('harmadik_aruhaz', token)

    if set.iweld_szinkron:
        nev = set.iweld_api_nev
        pas = set.iweld_api_pass
        iweld_stock_nagyker_szinkron(nev, pas)

    if set.Mastroweld_szinkron:
        mas_nagyker_szinkron()

    # Készlet beállítása
    if set.keszlet_to_unas_alap_aruhaz:
        keszlet_to_unas('alap_aruhaz')

    if set.keszlet_to_unas_masodik_aruhaz:
        keszlet_to_unas('masodik_aruhaz')

    if set.keszlet_to_unas_harmadik_aruhaz:
        keszlet_to_unas('harmadik_aruhaz')

    # print(adderrorlist)
    return HttpResponse('Siker', content_type="text/plain")