from django.contrib import admin
from .models import *


class BevetelAdmin(admin.ModelAdmin):
    list_display = ('bevetel_datum', 'szallitolevel_szam', 'beszallito', 'raktar', 'termek', 'bevetel_mennyiseg')
    list_filter = ('bevetel_datum','raktar','beszallito')
    def has_add_permission(self, request):
        return False
    # search_fields = ('tartozektipus',)


class BeallitasAndmin(admin.ModelAdmin):
    list_display = ('alap_aruhaz_nev',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj = None):
        return False


class ErtekesitAndmin(admin.ModelAdmin):
    list_display = ('eladas_datum','unas_order_key', 'termek', 'ar_eladas_brutto')
    search_fields = ['termek__termek_nev', 'termek__gyari_cikkszam']
    list_filter = ('eladas_datum',)
    autocomplete_fields = ['termek']


class TermekAdmin(admin.ModelAdmin):
    ordering = ['termek_nev']
    search_fields = ['termek_nev', 'gyari_cikkszam']
    def has_delete_permission(self, request, obj=None):
        return False

class RaktarkeszletAndmin(admin.ModelAdmin):
    list_display = ('termek','keszlet', 'raktar')
    search_fields = ['termek__termek_nev', 'termek__gyari_cikkszam']
    autocomplete_fields = ['termek']
    # list_filter = ('termek',)
    def has_delete_permission(self, request, obj=None):
        return False

class RaktarAndmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Bevetel, BevetelAdmin)
admin.site.register(Beallitas, BeallitasAndmin)
admin.site.register(Ertekesit, ErtekesitAndmin)
admin.site.register(Raktarkeszlet, RaktarkeszletAndmin)
admin.site.register(Termek, TermekAdmin)
admin.site.register(Raktar, RaktarAndmin)