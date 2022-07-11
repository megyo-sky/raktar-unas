from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from raktar.forms import BeszallitoForm
from raktar.forms import Beszallito
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers.json import DjangoJSONEncoder
import json


@login_required(login_url='/login/')
def beszallito_list(request):
    beszallitok_list = Beszallito.objects.all().values()
    beszallitok = json.dumps(list(beszallitok_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/beszallito_list.html',
        {
            'title': 'Beszállítók listája',
            'beszallitok': beszallitok,
        }
    )


@staff_member_required(login_url='/login/')
def beszallito_new(request):
    if request.method == "POST":
        form = BeszallitoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beszallito_list')
    else:
        form = BeszallitoForm()

    return render(
        request,
        'app/beszallito_new.html',
        {
            'title': 'Új beszállító létrehozása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def beszallito_edit(request, pk):
    beszallito = get_object_or_404(Beszallito, pk=pk)
    if request.method == "POST":
        form = BeszallitoForm(request.POST, instance=beszallito)
        if form.is_valid():
            form.save()
            return redirect('beszallito_list')
    else:
        form = BeszallitoForm(instance=beszallito)

    return render(
        request,
        'app/beszallito_edit.html',
        {
            'title': 'Beszállító módosítása',
            'form': form
        }
    )
