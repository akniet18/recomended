from django.contrib import admin
from locations.models import Country, City, Region

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Region)