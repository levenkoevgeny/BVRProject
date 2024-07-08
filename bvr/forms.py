from django.forms import ModelForm
from .models import ProcurementSector, Remains, CustomUser


class ProcurementSectorForm(ModelForm):
    class Meta:
        model = ProcurementSector
        fields = '__all__'


class RemainsForm(ModelForm):
    class Meta:
        model = Remains
        fields = '__all__'


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'