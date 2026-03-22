from django.urls import path
from .views import (
    AdminDashboardView,
    AdminBookListView, AdminBookCreateView, AdminBookEditView, AdminBookDeleteView,
    AdminCategoryListView, AdminCategoryCreateView, AdminCategoryEditView, AdminCategoryDeleteView,
    AdminUserListView,
    AdminOrderListView, AdminOrderDetailView,
)

urlpatterns = [
    # Dashboard
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),

    # Books
    path('books/', AdminBookListView.as_view(), name='admin_book_list'),
    path('books/add/', AdminBookCreateView.as_view(), name='admin_book_add'),
    path('books/<int:pk>/edit/', AdminBookEditView.as_view(), name='admin_book_edit'),
    path('books/<int:pk>/delete/', AdminBookDeleteView.as_view(), name='admin_book_delete'),

    # Categories
    path('categories/', AdminCategoryListView.as_view(), name='admin_category_list'),
    path('categories/add/', AdminCategoryCreateView.as_view(), name='admin_category_add'),
    path('categories/<int:pk>/edit/', AdminCategoryEditView.as_view(), name='admin_category_edit'),
    path('categories/<int:pk>/delete/', AdminCategoryDeleteView.as_view(), name='admin_category_delete'),

    # Users
    path('users/', AdminUserListView.as_view(), name='admin_user_list'),

    # Orders
    path('orders/', AdminOrderListView.as_view(), name='admin_order_list'),
    path('orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin_order_detail'),
]
