from django.http import HttpResponse
from raktar.models import keszlet_riport, termek_riport, bevetel_riport, ertekesit_riport
from django.contrib.auth.decorators import login_required
import xlwt
from django.contrib.admin.views.decorators import staff_member_required


# Exportok
@staff_member_required(login_url='/login/')
def export_termek(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="termek_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Termékek')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Azonosító', 'Termék név', 'Gyári cikkszám', 'Nagyker nettó ár', 'Bolti bruttó ár',
               'Elhelyezés', 'Minimum készlet', 'Mennyiségi egység', 'Termék gyártó', 'Termékkategória', 'Megjegyzés',
               'Aktív']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = termek_riport.objects.all().values_list('id', 'termek_nev', 'gyari_cikkszam', 'ar_web_netto', 'ar_bolt_brutto', 'elhelyezes', 'min_keszlet', 'mennyisegi_egyseg', 'termekgyarto', 'termekkategoria', 'megjegyzes', 'aktiv')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@staff_member_required(login_url='/login/')
def export_ertekesit(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ertekesites_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Értékesítések')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Azonosító', 'Termék neve', 'Gyári cikkszám', 'Saját cikkszám', 'Eladott mennyiség', 'Eladási ár', 'Eladás dátum',
               'Felhasználó', 'Megjegyzés']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = ertekesit_riport.objects.all().values_list('azonosito', 'termek_nev', 'gyari_cikkszam', 'sajat_cikkszam', 'eladas_mennyiseg', 'ar_eladas_brutto', 'eladas_datum', 'username', 'megjegyzes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@staff_member_required(login_url='/login/')
def export_bevetel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bevetelek_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Bevételezések')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Azonosító', 'Termék neve', 'Gyári cikkszám', 'Saját cikkszám', 'Beszállító neve',  'Raktár neve', 'Bevételezett mennyiség', 'Bevételezési nettó ár',
               'Bevételezés dátuma', 'Szállítólevél száma', 'Felhasználó', 'Megjegyzés']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = bevetel_riport.objects.all().values_list('azonosito', 'termek_nev', 'gyari_cikkszam', 'sajat_cikkszam', 'beszallito_nev', 'raktar_nev', 'bevetel_mennyiseg', 'ar_bevetel_netto', 'bevetel_datum', 'szallitolevel_szam', 'username', 'megjegyzes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@staff_member_required(login_url='/login/')
def export_raktarkeszlet(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="raktarkeszlet_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Raktárkészlet')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Termék azonosító', 'Terméknév', 'Gyári cikkszám', 'Saját cikkszám', 'Raktár név', 'Készlet',
               'Mennyiségi egység']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = keszlet_riport.objects.all().values_list('termek_id', 'termek_nev', 'gyari_cikkszam', 'sajat_cikkszam', 'raktar_nev', 'keszlet', 'mennyisegi_egyseg')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response