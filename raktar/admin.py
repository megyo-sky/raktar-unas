from django.contrib import admin
from .models import *
admin.site.register(Raktar)

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
    list_display = ('eladas_datum','unas_order_key', 'termek')
    search_fields = ['termek__termek_nev']
    list_filter = ('eladas_datum',)

class RaktarkeszletAndmin(admin.ModelAdmin):
    list_display = ('termek','keszlet', 'raktar')
    search_fields = ['termek__termek_nev']
    # list_filter = ('termek',)


admin.site.register(Bevetel, BevetelAdmin)
admin.site.register(Beallitas, BeallitasAndmin)
admin.site.register(Ertekesit, ErtekesitAndmin)
admin.site.register(Raktarkeszlet, RaktarkeszletAndmin)