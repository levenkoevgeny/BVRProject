from django.db import models
from django.contrib.auth.models import AbstractUser


class District(models.Model):
    district_name = models.CharField(max_length=255)

    def __str__(self):
        return self.district_name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        ordering = ("district_name",)


class ProcurementSector(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="District")
    sector_number = models.IntegerField(verbose_name="Sector Number")
    sector_address = models.TextField(verbose_name="Sector address")
    comments = models.TextField(verbose_name="Comments", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super(ProcurementSector, self).save(*args, **kwargs)
            print(Remains.objects.create(sector=self))
        else:
            super(ProcurementSector, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sector_number)

    class Meta:
        verbose_name = 'Участок заготовки'
        verbose_name_plural = 'Участки заготовки'
        ordering = ("sector_number",)


class CustomUser(AbstractUser):
    sector = models.OneToOneField(ProcurementSector, on_delete=models.CASCADE, verbose_name="Sector", blank=True,
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
    wastepaper_count = models.IntegerField(verbose_name="Макулатура (количество)", blank=True, null=True)
    wastepaper_needs_exportation = models.BooleanField(verbose_name="Макулатура (нужен вывоз)", default=False)
    cullet_count = models.IntegerField(verbose_name="Стеклобой (количество)", blank=True, null=True)
    cullet_needs_exportation = models.BooleanField(verbose_name="Стеклобой (нужен вывоз)", default=False)

    polyethylene_count = models.IntegerField(verbose_name="Полиэтилен (количество)", blank=True, null=True)
    polyethylene_needs_exportation = models.BooleanField(verbose_name="Полиэтилен (нужен вывоз)", default=False)

    scrap_metal_count = models.IntegerField(verbose_name="Металлолом (количество)", blank=True, null=True)
    scrap_metal_needs_exportation = models.BooleanField(verbose_name="Металлолом (нужен вывоз)", default=False)
    date_time_updated = models.DateTimeField(verbose_name="Дата и время последнего редактирования", auto_now=True)

    def __str__(self):
        return self.sector.sector_number

    class Meta:
        verbose_name = 'Остаток материальных ресурсов'
        verbose_name_plural = 'Остатки материальных ресурсов'
        ordering = ("-wastepaper_needs_exportation", "-cullet_needs_exportation", "-polyethylene_needs_exportation",
                    "-scrap_metal_needs_exportation")
