from django_filters import rest_framework as filters
from apps.news import models

BACKEND = filters.DjangoFilterBackend


class PostSearchFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    date = filters.DateFilter(lookup_expr='icontains')
    author = filters.CharFilter()

    class Meta:
        model = models.Publications
        fields = ['title', 'date']
