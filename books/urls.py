"""
Books URL patterns.
"""

from django.urls import path
from .views import (
    BookListView, BookDetailView,
    CategoryListView, CategoryBooksView,
    PDFViewerView, PDFServeView
)

urlpatterns = [
    # Book listing & detail
    path('', BookListView.as_view(), name='book_list'),
    path('<slug:slug>/', BookDetailView.as_view(), name='book_detail'),

    # PDF viewer & server
    path('<slug:slug>/read/', PDFViewerView.as_view(), name='pdf_viewer'),
    path('<slug:slug>/pdf/', PDFServeView.as_view(), name='pdf_serve'),

    # Categories — clean URLs: /category/science/
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryBooksView.as_view(), name='category_books'),
]
