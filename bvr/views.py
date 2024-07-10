from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator

from .models import CustomUser, Remains, ProcurementSector, District
from .forms import ProcurementSectorForm, RemainsForm, CustomUserForm
from .filters import CustomUserFilter, ProcurementSectorFilter, RemainsFilter
from django.core.exceptions import PermissionDenied


@login_required
def index(request):
    if request.user.is_superuser:
        return redirect('bvr:users')
    else:
        return redirect('bvr:remains-update-form', remain_id=request.user.sector.remains.id)


def init_db(request):
    if request.method == 'POST':
        pass
    else:
        CustomUser.objects.all().delete()
        District.objects.all().delete()
        ProcurementSector.objects.all().delete()
        Remains.objects.all().delete()
        admin_user = CustomUser.objects.create_user("admin", "", "12345678")
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.last_name = "Администратор"
        admin_user.save()

        import csv
        with open('1.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                new_district, created = District.objects.get_or_create(district_name=row[3])
                print('new_district', new_district)
                new_sector = ProcurementSector.objects.create(district=new_district, sector_number=row[1],
                                                              sector_address=row[0])
                new_user = CustomUser.objects.create_user(row[1], "", row[2])
                new_user.sector = new_sector
                new_user.last_name = row[1]
                new_user.save()

        return HttpResponse("DB init is completed!!!")


@login_required
def user_list(request):
    request.session['back_path'] = '/bvr/users?' + request.META.get('QUERY_STRING')
    qs = CustomUser.objects.all()
    if 'o' in request.GET:
        order_query = request.GET['o'].split('.')
        qs = qs.order_by(*order_query)
    f = CustomUserFilter(request.GET, queryset=qs)
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    users_list = paginator.get_page(page)
    return render(request, 'bvr/users/users_list.html', {'users_list': users_list, 'filter': f})


# @login_required
# def user_add(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('bvr:users'))
#         else:
#             return render(request, 'bvr/users/user_input_form.html', {'user_form': form})
#     if request.method == 'GET':
#         applicant_form = CustomUserForm()
#         return render(request, 'bvr/users/user_input_form.html', {'applicant_form': applicant_form})
#     else:
#         pass


@login_required
def user_update(request, user_id):
    if request.method == 'POST':
        obj = get_object_or_404(CustomUser, pk=user_id)
        print('obj', obj.username)

        form = CustomUserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            back_path = request.session.get('back_path', '/')
            return HttpResponseRedirect(back_path)
        else:
            print(form.errors)
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
    request.session['back_path'] = '/bvr/sectors?' + request.META.get('QUERY_STRING')
    qs = ProcurementSector.objects.all()
    if 'o' in request.GET:
        order_query = request.GET['o'].split('.')
        qs = qs.order_by(*order_query)
    f = ProcurementSectorFilter(request.GET, queryset=qs)
    paginator = Paginator(f.qs, 50)
    page = request.GET.get('page')
    sectors_list = paginator.get_page(page)
    return render(request, 'bvr/sectors/sectors_list.html', {'sectors_list': sectors_list, 'filter': f})


@login_required
def sector_add(request):
    if request.method == 'POST':
        form = ProcurementSectorForm(request.POST)
        if form.is_valid():
            new_sector = form.save()
            password = request.POST.get('password')
            new_user = CustomUser.objects.create_user(new_sector.sector_number, "", password)
            new_user.sector = new_sector
            new_user.last_name = new_sector.sector_number
            new_user.save()
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
        request.session['back_path'] = '/bvr/remains?' + request.META.get('QUERY_STRING')
        qs = Remains.objects.filter(sector__customuser__is_active=True)
        if 'o' in request.GET:
            order_query = request.GET['o'].split('.')
            qs = qs.order_by(*order_query)
        f = RemainsFilter(request.GET, queryset=qs)
        paginator = Paginator(f.qs, 50)
        page = request.GET.get('page')
        remains_list = paginator.get_page(page)
        return render(request, 'bvr/remains/remains_list.html', {'remains_list': remains_list, 'filter': f})
    else:
        raise PermissionDenied()


@login_required
def remain_update(request, remain_id):
    if request.method == 'POST':
        obj = get_object_or_404(Remains, pk=remain_id)
        form = RemainsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                back_path = request.session.get('back_path', '/')
                return HttpResponseRedirect(back_path)
            else:
                return redirect('bvr:remains-update-form', remain_id=request.user.sector.remains.id)
        else:
            return render(request, 'bvr/remains/remains_input_form.html', {'remain_form': form,
                                                                           'obj': obj,
                                                                           })
    else:
        current_user = request.user
        remains = get_object_or_404(Remains, pk=remain_id)
        form = RemainsForm(instance=remains)
        if request.user.is_superuser:
            return render(request, 'bvr/remains/remains_update_form.html', {'remain_form': form,
                                                                            'remains': remains})
        else:
            if remains.sector.customuser == current_user:
                return render(request, 'bvr/remains/remains_update_form.html', {'remain_form': form,
                                                                                'remains': remains})
            else:
                raise PermissionDenied()
