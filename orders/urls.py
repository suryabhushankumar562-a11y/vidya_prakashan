from django.urls import path
from .views import CheckoutView, OrderConfirmationView, OrderHistoryView, OrderDetailView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('confirmation/<str:order_number>/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('history/', OrderHistoryView.as_view(), name='order_history'),
    path('<str:order_number>/', OrderDetailView.as_view(), name='order_detail'),
]
