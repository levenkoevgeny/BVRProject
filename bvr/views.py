from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import CustomUser, Remains, ProcurementSector
from .forms import ProcurementSectorForm, RemainsForm, CustomUserForm
from .filters import CustomUserFilter


@login_required
def index(request):
    if request.user.is_superuser:
        return redirect('bvr:users')
    else:
        return redirect('bvr:remains')


@login_required
def user_list(request):
    request.session['back_path'] = '/users/?' + request.META.get('QUERY_STRING')
    qs = CustomUser.objects.all()
    if 'o' in request.GET:
        order_query = request.GET['o'].split('.')
        qs = qs.order_by(*order_query)
    f = CustomUserFilter(request.GET, queryset=qs)
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    users_list = paginator.get_page(page)
    return render(request, 'bvr/users/users_list.html', {'users_list': users_list, 'filter': f})


@login_required
def user_add(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bvr:users'))
        else:
            return render(request, 'bvr/users/user_input_form.html', {'user_form': form})
    if request.method == 'GET':
        applicant_form = CustomUserForm()
        return render(request, 'bvr/users/user_input_form.html', {'applicant_form': applicant_form})
    else:
        pass


@login_required
def user_update(request, user_id):
    if request.method == 'POST':
        obj = get_object_or_404(CustomUser, pk=user_id)
        form = CustomUserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            back_path = request.session.get('back_path', '/')
            return HttpResponseRedirect(back_path)
        else:
            return render(request, 'bvr/users/user_update_form.html', {'user_form': form,
                                                                  'obj': obj,
                                                                  })
    else:
        obj = get_object_or_404(CustomUser, pk=user_id)
        form = CustomUserForm(instance=obj)
        return render(request, 'bvr/users/user_update_form.html', {'user_form': form,
                                                              'obj': obj})




@login_required
def sector_list(request):
    sectors_list = ProcurementSector.objects.all()
    return render(request, 'bvr/sectors/sectors_list.html', {'sectors_list': sectors_list})


@login_required
def sector_add(request):
    if request.method == 'POST':
        form = ProcurementSectorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('bvr:sectors'))
        else:
            return render(request, 'bvr/sectors/sector_input_form.html', {'sector_form': form})
    if request.method == 'GET':
        form = ProcurementSectorForm()
        return render(request, 'bvr/sectors/sector_input_form.html', {'sector_form': form})
    else:
        pass


@login_required
def sector_update(request, sector_id):
    if request.method == 'POST':
        obj = get_object_or_404(ProcurementSector, pk=sector_id)
        form = ProcurementSectorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            back_path = request.session.get('back_path', '/')
            return HttpResponseRedirect(back_path)
        else:
            return render(request, 'bvr/sectors/sector_update_form.html', {'sector_form': form,
                                                                  'obj': obj,
                                                                  })
    else:
        obj = get_object_or_404(ProcurementSector, pk=sector_id)
        form = ProcurementSectorForm(instance=obj)
        return render(request, 'bvr/sectors/sector_update_form.html', {'sector_form': form,
                                                              'obj': obj})


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
def remain_add(request):
    pass
    # if request.method == 'POST':
    #     form = ProcurementSectorForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('bvr:sectors'))
    #     else:
    #         return render(request, 'bvr/sectors/sector_input_form.html', {'sector_form': form})
    # if request.method == 'GET':
    #     form = ProcurementSectorForm()
    #     return render(request, 'bvr/sectors/sector_input_form.html', {'sector_form': form})
    # else:
    #     pass


@login_required
def remain_update(request, sector_id):
    pass
    # if request.method == 'POST':
    #     obj = get_object_or_404(ProcurementSector, pk=sector_id)
    #     form = ProcurementSectorForm(request.POST, instance=obj)
    #     if form.is_valid():
    #         form.save()
    #         back_path = request.session.get('back_path', '/')
    #         return HttpResponseRedirect(back_path)
    #     else:
    #         return render(request, 'bvr/sectors/sector_update_form.html', {'sector_form': form,
    #                                                               'obj': obj,
    #                                                               })
    # else:
    #     obj = get_object_or_404(CustomUser, pk=sector_id)
    #     form = ProcurementSectorForm(instance=obj)
    #     return render(request, 'bvr/users/sectors/sector_update_form.html', {'sector_form': form,
    #                                                           'obj': obj})
