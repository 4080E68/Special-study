from .models import *
import django_filters
from django import forms


class cpuFilter(django_filters.FilterSet):

    vendor = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    price = django_filters.CharFilter(lookup_expr='lte')
        
    

    class Meta:
        model = cpu
        fields = '__all__'
