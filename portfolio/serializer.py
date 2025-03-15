from rest_framework import serializers
from .models import Portfolio
from property.models import Property

class PortfolioListSerializer(serializers.ModelSerializer):
    class PropertySerializer(serializers.ModelSerializer):
        class Meta:
            model = Property
            fields = (
                'id',
                'address',
                'zip_code',
                'zip_place',
                )

    properties = PropertySerializer(many=True, read_only=True, source='property')
    class Meta:
        model=Portfolio
        fields=(
            'id',
            'name',
            'owner_of_portfolio',
            'properties',
            )

class PortfolioReadSerializer(serializers.ModelSerializer):
    class PropertySerializer(serializers.ModelSerializer):
        class Meta:
            model = Property
            fields = (
                'id',
                'address',
                'zip_code',
                'zip_place',
                'estimated_value',
                'construction_year',
                'usable_area',
                'image',
                )

    properties = PropertySerializer(many=True, read_only=True, source='property')
    class Meta:
        model=Portfolio
        fields=(
            'id',
            'name',
            'owner_of_portfolio',
            'geographic_region',
            'image',
            'properties',
            )
        
class PortfolioEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=Portfolio
        fields=(
            'name',
            'owner_of_portfolio',
            'geographic_region',
            'image',
            )

    def validate_image(self, value):
        if value == "null" or value is None:
            return None
        
        return value 