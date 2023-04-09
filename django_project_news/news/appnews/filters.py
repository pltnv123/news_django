import django_filters
from django_filters import FilterSet, ModelChoiceFilter, ChoiceFilter
from .models import Post, Category, PostCategory
from django.forms import DateTimeInput, DateInput


class PostFilter(FilterSet):
    added_after = django_filters.DateFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата',
        widget=DateInput(
            attrs={'type': 'date'},
        ),
    )

    rank = ChoiceFilter(
        field_name='categoryType',
        # queryset=Post.categoryType.objects.all(),
        label='Тип поста:',
        # emty_label='Select type',
        choices=Post.CATEGORY_CHOIESES
    )

    category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категории:'
    )

    # title_list = django_filters.ModelChoiceFilter(
    #     field_name='title',
    #     queryset=Post.objects.all(),
    #     label='Посты:',
    # )

    title_search = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Поиск по постам:',
    )

    # class Meta:
    #     model = Post
    #     fields = {
    #         # 'title': ['icontains'],
    #     }
