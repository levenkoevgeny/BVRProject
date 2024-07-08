import django_filters
from django import forms

from .models import CustomUser, ProcurementSector, Remains

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class CustomUserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    is_superuser = django_filters.BooleanFilter(field_name='is_superuser')
    class Meta:
        model = CustomUser
        fields = []


class ProcurementSectorFilter(django_filters.FilterSet):
    pass

    class Meta:
        model = ProcurementSector
        fields = []


class RemainsFilter(django_filters.FilterSet):
    pass

    class Meta:
        model = Remains
        fields = []