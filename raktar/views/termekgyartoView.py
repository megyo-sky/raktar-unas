from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from raktar.forms import TermekGyartoForm
from raktar.models import TermekGyarto
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='/login/')
def termekgyarto_list(request):
    # termekkategoria_list = TermekKategoria.objects.all().values()
    # termekkategoria = json.dumps(list(termekkategoria_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/termekgyarto_list.html',
        {
            'title': 'Termék gyártók listája',
            # 'termekkategoria': termekkategoria,
        }
    )


@staff_member_required(login_url='/login/')
def termekgyarto_new(request):
    if request.method == "POST":
        form = TermekGyartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('termekgyarto_list')
    else:
        form = TermekGyartoForm()

    return render(
        request,
        'app/termekgyarto_new.html',
        {
            'title': 'Új termék gyártó létrehozása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termekgyarto_edit(request, pk):
    termekgyarto = get_object_or_404(TermekGyarto, pk=pk)
    if request.method == "POST":
        form = TermekGyartoForm(request.POST, instance=termekgyarto)
        if form.is_valid():
            form.save()
            return redirect('termekgyarto_list')
    else:
        form = TermekGyartoForm(instance=termekgyarto)

    return render(
        request,
        'app/termekgyarto_edit.html',
        {
            'title': 'Termék gyártó módosítása',
            'form': form
        }
    )