from django.contrib import admin
from .models import CustomUser, ProcurementSector, Remains


admin.site.register(CustomUser)
admin.site.register(ProcurementSector)
admin.site.register(Remains)
