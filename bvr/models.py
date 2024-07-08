from django.db import models
from django.contrib.auth.models import AbstractUser


# class District(models.Model):
#     district_name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.district_name
#
#     class Meta:
#         verbose_name = 'Город'
#         verbose_name_plural = 'Города'
#         ordering = ("district_name",)


class ProcurementSector(models.Model):
    sector_number = models.CharField(max_length=50, verbose_name="Sector Number")
    sector_address = models.TextField(verbose_name="Sector address", blank=True, null=True)
    comments = models.TextField(verbose_name="Comments", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super(ProcurementSector, self).save(*args, **kwargs)
            print(Remains.objects.create(sector=self))
        else:
            super(ProcurementSector, self).save(*args, **kwargs)

    def __str__(self):
        return self.sector_number

    class Meta:
        verbose_name = 'Участок заготовки'
        verbose_name_plural = 'Участки заготовки'
        ordering = ("sector_number",)


class CustomUser(AbstractUser):
    sector = models.ForeignKey(ProcurementSector, on_delete=models.CASCADE, verbose_name="Sector", blank=True,
                               null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("username",)


class Remains(models.Model):
    sector = models.OneToOneField(ProcurementSector, on_delete=models.CASCADE, verbose_name="Sector", blank=True,
                                  null=True)
    wastepaper_count = models.IntegerField(verbose_name="Макулатура (количество)", default=0)
    wastepaper_needs_exportation = models.BooleanField(verbose_name="Макулатура (нужен вывоз)", default=False)
    cullet_count = models.IntegerField(verbose_name="Стеклобой (количество)", default=0)
    cullet_needs_exportation = models.BooleanField(verbose_name="Стеклобой (нужен вывоз)", default=False)

    polyethylene_count = models.IntegerField(verbose_name="Полиэтилен (количество)", default=0)
    polyethylene_needs_exportation = models.BooleanField(verbose_name="Полиэтилен (нужен вывоз)", default=False)

    scrap_metal_count = models.IntegerField(verbose_name="Металлолом (количество)", default=0)
    scrap_metal_needs_exportation = models.BooleanField(verbose_name="Металлолом (нужен вывоз)", default=False)
    date_time_updated = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True)

    def __str__(self):
        return self.sector.sector_number

    class Meta:
        verbose_name = 'Остаток материальных ресурсов'
        verbose_name_plural = 'Остатки материальных ресурсов'
        ordering = ("sector",)
