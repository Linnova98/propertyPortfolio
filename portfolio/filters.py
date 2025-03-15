import django_filters
from .models import Portfolio
from django.db.models import Q

class PortfolioFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Filter by Name")
    owner_of_portfolio = django_filters.CharFilter(lookup_expr='icontains', label="Filter by Owner")
    geographic_region = django_filters.CharFilter(lookup_expr='icontains', label="Filter by Region")
    search = django_filters.CharFilter(method='filter_by_search', label="Search across all fields")
    
    
    class Meta:
        model = Portfolio
        fields = ['name', 'owner_of_portfolio', 'geographic_region']

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(owner_of_portfolio__icontains=value) | Q(geographic_region__icontains=value)
        )
