import datetime
import os
from raktar.models import Termek, Beallitas
from django.conf import settings
import xml.etree.ElementTree as et
import requests, csv
from django.shortcuts import render, redirect
from django.http import HttpResponse


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
            Termek.objects.update(alap_aruhaz = 0, alap_bolt_ar_brutto = 0)
        else:
            Termek.objects.update(alap_aruhaz=0)
        Beallitas.objects.filter(id=1).update(alap_aruhaz_clean = 0)

    elif aruhaz == "masodik_aruhaz":
        if set.masodik_aruhaz_clean:
            Termek.objects.update(masodik_aruhaz = 0, masodik_bolt_ar_brutto = 0)
        else:
            Termek.objects.update(masodik_aruhaz=0)
        Beallitas.objects.filter(id=1).update(masodik_aruhaz_clean=0)

    elif aruhaz == "harmadik_aruhaz":
        if set.harmadik_aruhaz_clean:
            Termek.objects.update(harmadik_aruhaz = 0, harmadik_bolt_ar_brutto = 0)
        else:
            Termek.objects.update(harmadik_aruhaz=0)
        Beallitas.objects.filter(id=1).update(harmadik_aruhaz_clean=0)

    print("Dataclean kész " + aruhaz)


def unas_betolto(aruhaz):
    set = Beallitas.objects.get(id=1)
    xml = str(os.path.join(settings.MEDIA_ROOT) + '/import/'+aruhaz+'_termek_import.xml')
    tree = et.parse(xml)
    root = tree.getroot()
    # print(root.tag)
    list=[]
    for child in root:
        state = (child.find('State').text)
        if state != 'deleted':
            cikkszam = (child.find('Sku').text)
            name = (child.find('Name').text)
            egyseg = (child.find('Unit').text)
            price = int(float(child.find('Prices')[1].find('Gross').text))

            if Termek.objects.filter(gyari_cikkszam = cikkszam).exists():
                if aruhaz == "alap_aruhaz":
                    if set.alap_aruhaz_kezdeti_arszinkron:
                        Termek.objects.filter(gyari_cikkszam = cikkszam).update(alap_aruhaz=True, alap_bolt_ar_brutto=price)
                    else:
                        Termek.objects.filter(gyari_cikkszam=cikkszam).update(alap_aruhaz=True)

                elif aruhaz == "masodik_aruhaz":
                    if set.masodik_aruhaz_kezdeti_arszinkron:
                        Termek.objects.filter(gyari_cikkszam = cikkszam).update(masodik_aruhaz=True, masodik_bolt_ar_brutto=price)
                    else:
                        Termek.objects.filter(gyari_cikkszam = cikkszam).update(masodik_aruhaz=True)

                elif aruhaz == "harmadik_aruhaz":
                    if set.harmadik_aruhaz_kezdeti_arszinkron:
                        Termek.objects.filter(gyari_cikkszam = cikkszam).update(harmadik_aruhaz=True, harmadik_bolt_ar_brutto=price)
                    else:
                        Termek.objects.filter(gyari_cikkszam = cikkszam).update(harmadik_aruhaz=True)

            else:
                if aruhaz == "alap_aruhaz":
                    list.append(Termek(gyari_cikkszam=cikkszam, termek_nev=name, alap_bolt_ar_brutto=price,mennyisegi_egyseg=egyseg, alap_aruhaz=True),)
                elif aruhaz == "masodik_aruhaz":
                    list.append(Termek(gyari_cikkszam=cikkszam, termek_nev=name, masodik_bolt_ar_brutto=price, mennyisegi_egyseg=egyseg,masodik_aruhaz=True),)
                elif aruhaz == "harmadik_aruhaz":
                    list.append(
                        Termek(gyari_cikkszam=cikkszam, termek_nev=name, harmadik_bolt_ar_brutto=price, mennyisegi_egyseg=egyseg,harmadik_aruhaz=True),)

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

def unas_price_update(aruhaz, token):
    urlToken = 'https://api.unas.eu/shop/setProduct'
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'text/xml'}
    param = '<Products>'

    if aruhaz == "alap_aruhaz":
        termekek = 	Termek.objects.filter(alap_aruhaz=True).values_list('gyari_cikkszam', 'alap_bolt_ar_brutto')
    elif aruhaz == "masodik_aruhaz":
        termekek = 	Termek.objects.filter(masodik_aruhaz=True).values_list('gyari_cikkszam', 'masodik_bolt_ar_brutto')
    elif aruhaz == "harmadik_aruhaz":
        termekek = 	Termek.objects.filter(harmadik_aruhaz=True).values_list('gyari_cikkszam', 'harmadik_bolt_ar_brutto')
    for row in termekek:
        sku = row[0]
        price = row[1]
        if (price != 0) and (price is not None):
            price = str(row[1])
            param += '<Product><Action>modify</Action><Sku>'+sku+'</Sku><Prices><Price><Type>normal</Type><Net>'+price+'</Net><Gross>'+price+'</Gross></Price></Prices></Product>'
    param += '</Products>'
    print(param)
    response = requests.get(urlToken, data=param, headers=headers)
    if response.status_code == requests.codes.ok:
         print(response.text)
    else:
        print(response.text)


    print("Ár módosítás kész: " + aruhaz)


def mas_download():
    url = 'https://www.mastroweld.hu/files/csv_export/sajat.csv'
    data = requests.get(url)
    data.encoding = 'utf-8'
    lines = data.text.splitlines()
    reader = csv.reader(lines, delimiter=';')
    for row in reader:
        sku=row[0]
        keszlet= row[5]
        netto_ar=row[8]

        print(" sku: "+sku+" --- keszlet: "+keszlet+" ---ar: "+netto_ar)


def szinkron(request):
    mas_download()

    # set = Beallitas.objects.get(id=1)
    #
    # if set.alap_aruhaz_aktiv:
    #     dataclean('alap_aruhaz')
    #     token = getUnasToken('alap_aruhaz')
    #     unas_download('alap_aruhaz', token)
    #     unas_betolto('alap_aruhaz')
    #     # unas_price_update('alap_aruhaz', token)
    #
    #
    # if set.masodik_aruhaz_aktiv:
    #     dataclean('masodik_aruhaz')
    #     token = getUnasToken('masodik_aruhaz')
    #     unas_download('masodik_aruhaz', token)
    #     unas_betolto('masodik_aruhaz')
    #     # unas_price_update('masodik_aruhaz', token)
    #
    #
    # if set.harmadik_aruhaz_aktiv:
    #     dataclean('harmadik_aruhaz')
    #     token = getUnasToken('harmadik_aruhaz')
    #     unas_download('harmadik_aruhaz', token)
    #     unas_betolto('harmadik_aruhaz')
    #     # unas_price_update('harmadik_aruhaz', token)



    return HttpResponse('Siker', content_type="text/plain")