"""
Pagination classes for Knowledge Base API
"""
from rest_framework.pagination import PageNumberPagination


class KnowledgeBasePagination(PageNumberPagination):
    """
    Custom pagination class for Knowledge Base API endpoints.
    Returns 100 items per page by default.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
