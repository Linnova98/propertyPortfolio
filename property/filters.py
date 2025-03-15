import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    min_value = django_filters.NumberFilter(field_name="estimated_value", lookup_expr="gte")
    max_value = django_filters.NumberFilter(field_name="estimated_value", lookup_expr="lte")
    min_year = django_filters.NumberFilter(field_name="construction_year", lookup_expr="gte")
    max_year = django_filters.NumberFilter(field_name="construction_year", lookup_expr="lte")
    zip_code = django_filters.CharFilter(field_name="zip_code")
    zip_place = django_filters.CharFilter(field_name="zip_place", lookup_expr="icontains")
    address = django_filters.CharFilter(field_name="address", lookup_expr="icontains")
    portfolio = django_filters.NumberFilter(field_name="portfolio__id")

    class Meta:
        model = Property
        fields = ["min_value", "max_value", "min_year", "max_year", "zip_code", "zip_place", "address", "portfolio"]
