from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, UpdateCartView, ClearCartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update/<int:item_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('clear/', ClearCartView.as_view(), name='clear_cart'),
]
