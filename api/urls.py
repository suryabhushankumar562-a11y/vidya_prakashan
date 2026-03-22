"""
API URL patterns.
All endpoints prefixed with /api/
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterAPIView, UserProfileAPIView,
    BookListAPIView, BookDetailAPIView,
    CategoryListAPIView, CategoryBooksAPIView,
    CartAPIView, CartItemDeleteAPIView,
    OrderListAPIView, OrderDetailAPIView,
    PDFAccessAPIView,
)

urlpatterns = [
    # ── Authentication ──────────────────────────────────────────────
    path('auth/register/', RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api_login'),        # JWT login
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('auth/me/', UserProfileAPIView.as_view(), name='api_me'),

    # ── Books ───────────────────────────────────────────────────────
    path('books/', BookListAPIView.as_view(), name='api_book_list'),
    path('books/<slug:slug>/', BookDetailAPIView.as_view(), name='api_book_detail'),
    path('books/<slug:slug>/pdf-access/', PDFAccessAPIView.as_view(), name='api_pdf_access'),

    # ── Categories ──────────────────────────────────────────────────
    path('categories/', CategoryListAPIView.as_view(), name='api_category_list'),
    path('categories/<slug:slug>/books/', CategoryBooksAPIView.as_view(), name='api_category_books'),

    # ── Cart ────────────────────────────────────────────────────────
    path('cart/', CartAPIView.as_view(), name='api_cart'),
    path('cart/<int:item_id>/', CartItemDeleteAPIView.as_view(), name='api_cart_item_delete'),

    # ── Orders ──────────────────────────────────────────────────────
    path('orders/', OrderListAPIView.as_view(), name='api_order_list'),
    path('orders/<str:order_number>/', OrderDetailAPIView.as_view(), name='api_order_detail'),
]
