from django_filters import FilterSet, CharFilter, DateFilter, DateTimeFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):

    title = CharFilter(field_name='title', lookup_expr='contains', label='Поиск по названию')
    author__user__username = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Поиск по автору')
    time_date = DateTimeFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte', label='По дате'
    )

    # time_date = DateFilter(field_name='time_date', lookup_expr='gte', label='Поиск по дате')

    class Meta:
        model = Post
        fields = {
            'title',
            'author__user__username',
            # 'time_date'
        }