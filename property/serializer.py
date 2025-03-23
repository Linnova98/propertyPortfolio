from rest_framework import serializers
from .models import Property
from portfolio.models import Portfolio
import re

class PropertyListSerializer(serializers.ModelSerializer):
    class PortfolioSerializer(serializers.ModelSerializer):
        class Meta:
            model = Portfolio
            fields = (
                'id',
                'geographic_region',
                )
    
    portfolio = PortfolioSerializer(read_only=True) 
    
    class Meta:
        model=Property
        fields=(
            'id',
            'address',
            'zip_code',
            'zip_place',
            'portfolio',
            )

class PropertyReadSerializer(serializers.ModelSerializer):
    class PortfolioSerializer(serializers.ModelSerializer):
        class Meta:
            model = Portfolio
            fields = (
                'id',
                'name',
                'geographic_region',
                'owner_of_portfolio',
                'image',
                )
    
    portfolio = PortfolioSerializer(read_only=True) 
    
    class Meta:
        model=Property
        fields=(
            'id',
            'address',
            'zip_code',
            'zip_place',
            'estimated_value',
            'construction_year',
            'usable_area',
            'image',
            'portfolio',
            )

class PropertyEditSerializer(serializers.ModelSerializer):
    portfolio = serializers.PrimaryKeyRelatedField(queryset=Portfolio.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Property
        fields = (
            'address',
            'zip_code',
            'zip_place',
            'estimated_value',
            'construction_year',
            'usable_area',
            'image',
            'portfolio',
        )
        
    def validate_zip_code(self, value):
        if not re.fullmatch(r'\d{4}', value):
            raise serializers.ValidationError("Zip code must be exactly 4 digits.")
        return value

    def validate_usable_area(self, value):
        if value <= 0:
            raise serializers.ValidationError("Usable area must be greater than zero.")
        return value

    def validate_construction_year(self, value):
        if value < 1000 or value > 9999:
            raise serializers.ValidationError(f"Construction year must be 4 digits.")
        if not isinstance(value, int):
            raise serializers.ValidationError("Construction year must be an integer, no decimals allowed.")
        return value
    
    def validate_image(self, value):
        if value == "null" or value is None:
            return None
        
        return value