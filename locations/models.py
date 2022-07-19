from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    title_en = models.CharField(max_length=128, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.title


class Region(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.title


class City(models.Model):
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.title
