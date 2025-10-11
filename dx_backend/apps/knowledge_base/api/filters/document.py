from django_filters import rest_framework as filters

from apps.knowledge_base.models import Document


class DocumentFilter(filters.FilterSet):
    """
    Custom filter set for Document model.
    Allows filtering by title, content (search), and categories.
    """
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    content = filters.CharFilter(field_name='content', lookup_expr='icontains')
    categories = filters.CharFilter(field_name='categories__name', lookup_expr='exact')
    
    class Meta:
        model = Document
        fields = ['title', 'content', 'categories']
