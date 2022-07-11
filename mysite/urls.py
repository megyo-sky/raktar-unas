"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_raktar import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_raktar.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from datetime import datetime
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from raktar.views import TermekAutocomplete
from raktar.views import BeszallitoAutocomplete
import raktar.views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name= "app/login.html"),
         # athentication_form= raktar.forms.BootstrapAuthenticationForm),
         # 'extra_context':
         #    {
         #        'title': 'Log in',
         #        'year': datetime.now().year,
         #    }

        name='login'),

    # path('logout/', LogoutView.as_view(), next_page=None,  name='logout'),
    path('logout', LogoutView.as_view(), name='logout'),
    #
    # Uncomment the admin/doc line below to enable admin documentation:
    # path('admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('password/', raktar.views.change_password, name='change_password'),
    # path('accounts/', include('django.contrib.auth.urls')),

    # API URL
    # Termék értékesítés termék keresés
    path('api/get_termek/', raktar.views.get_termek, name='get_termek'),

    path('termek-autocomplete/', TermekAutocomplete.as_view(), name='termek-autocomplete', ),

    # Bevételezés beszállító keresés
    path('beszallito-autocomplete/', BeszallitoAutocomplete.as_view(), name='beszallito-autocomplete', ),

    # Termékek lista
    path('api/get_termekapi/', raktar.views.get_termek_api, name='get_termekapi'),

    # Termékkategórai lista
    path('api/get_termekkategoria_api/', raktar.views.get_termekkategoria_api, name='get_termekkategoria_api'),

    # Termék gyarto lista
    path('api/get_termekgyarto_api/', raktar.views.get_termekgyarto_api, name='get_termekgyarto_api'),

  # Alap URL
    path('', raktar.views.index, name='index'),
    path('beszallito/', raktar.views.beszallito_list, name='beszallito_list'),
    path('beszallito/new', raktar.views.beszallito_new, name='beszallito_new'),
    path('beszallito/<int:pk>/edit', raktar.views.beszallito_edit, name='beszallito_edit'),
    path('bevetel/new', raktar.views.bevetel_new, name='bevetel_new'),

    path('termek/', raktar.views.termek_list, name='termek_list'),
    path('termek/new', raktar.views.termek_new, name='termek_new'),
    path('termek/<int:pk>/edit', raktar.views.termek_edit, name='termk_edit'),

    path('termek-ertekesites/<int:pk>/show/', raktar.views.termek_ertekesites, name='termek_ertekesites'),
    path('termekatvezetes', raktar.views.termek_atvezetes, name='termek_atvezetes'),

    path('termekkategoria/', raktar.views.termekkategoria_list, name='termekkategoria_list'),
    path('termekkategoria/new', raktar.views.termekkategoria_new, name='termekkategoria_new'),
    path('termekkategoria/<int:pk>/edit', raktar.views.termekkategoria_edit, name='termekkategoria_edit'),

    path('termekgyarto/', raktar.views.termekgyarto_list, name='termekgyarto_list'),
    path('termekgyarto/new', raktar.views.termekgyarto_new, name='termekgyarto_new'),
    path('termekgyarto/<int:pk>/edit', raktar.views.termekgyarto_edit, name='termekgyarto_edit'),

    path('dokumentum/<int:pk>/list', raktar.views.dok_list, name='dok_list'),
    path('dokumentum/<int:pk>/new', raktar.views.dok_new, name='dok_new'),
    path('dokumentum/<int:pk>/<int:termek_id>/del', raktar.views.dok_del, name='dok_del'),

    path('termekimportfel/', raktar.views.termek_import_feltolt, name='termek_import_feltolt'),
    path('termekimport/', raktar.views.termek_import, name='termek_import'),

    path('arimportfel/', raktar.views.ar_import_feltolt, name='ar_import_feltolt'),
    path('arimport/', raktar.views.ar_import, name='ar_import'),

    path('webarmod/', raktar.views.web_ar_mod, name='web_ar_mod'),
    path('email/', raktar.views.email, name='email'),
    path('termekosszdb/', raktar.views.email_termek_osszdb, name='email_termek_osszdb'),

    # Export URL
    path('export_termek/', raktar.views.export_termek, name='export_termek'),
    path('export_ertekesit/', raktar.views.export_ertekesit, name='export_ertekesit'),
    path('export_bevetel/', raktar.views.export_bevetel, name='export_bevetel'),
    path('export_raktarkeszlet/', raktar.views.export_raktarkeszlet, name='export_raktarkeszlet'),

    path('tes/', raktar.views.szinkron, name='szinkron'),
    path('__debug__/', include(debug_toolbar.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
