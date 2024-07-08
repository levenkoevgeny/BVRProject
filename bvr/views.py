from django.shortcuts import render
from .models import CustomUser, Remains, ProcurementSector
from .forms import ProcurementSectorForm, RemainsForm, CustomUserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def index(request):
    if request.user.is_superuser:
        return redirect('bvr:users')
    else:
        return redirect('bvr:remains')


@login_required
def user_list(request):
    users_list = CustomUser.objects.all()
    return render(request, 'bvr/users/users_list.html', {'users_list': users_list})


@login_required
def remain_list(request):
    if request.user.is_superuser:
        remains_list = Remains.objects.all()
        return render(request, 'bvr/remains/remains_list.html', {'remains_list': remains_list})
    else:
        try:
            sector = ProcurementSector.objects.get(customuser=request.user)
            form = RemainsForm(instance=sector.remains)
            return render(request, 'bvr/remains/remains_input_form.html',
                          {'remain_form': form, 'last_updated': sector.remains.date_time_updated})
        except ProcurementSector.DoesNotExist:
            return render(request, 'bvr/remains/remains_input_form.html')


@login_required
def sector_list(request):
    sectors_list = ProcurementSector.objects.all()
    return render(request, 'bvr/sectors/sectors_list.html', {'sectors_list': sectors_list})
