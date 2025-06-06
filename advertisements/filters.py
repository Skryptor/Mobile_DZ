from django_filters import rest_framework as filters
from .models import Advertisement

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    status = filters.CharFilter(field_name='status')
    creator = filters.NumberFilter(field_name='creator__id')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'title', 'description', 'price_min', 'price_max']
