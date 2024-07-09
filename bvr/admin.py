from django.contrib import admin
from .models import CustomUser, District, ProcurementSector, Remains


admin.site.register(CustomUser)
admin.site.register(District)
admin.site.register(ProcurementSector)
admin.site.register(Remains)
