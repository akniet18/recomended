from rest_framework import serializers
from locations.models import Country, City, Region


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'code', 'title', 'title_en', 'flag')
        read_only_fields = ('id',)


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    class Meta:
        model = City
        fields = ('id', 'title', 'title_en', 'country')
        read_only_fields = ('id',)
