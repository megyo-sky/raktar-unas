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

class ErtekesitAndmin(admin.ModelAdmin):
    list_display = ('eladas_datum',)

admin.site.register(Bevetel, BevetelAdmin)
admin.site.register(Beallitas, BeallitasAndmin)
admin.site.register(Ertekesit, ErtekesitAndmin)