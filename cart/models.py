"""
Cart Models — Cart and CartItem for managing the shopping basket.
"""

from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Cart(models.Model):
    """
    Each logged-in user gets one Cart.
    Cart is cleared after order is placed.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        """Calculate the total price of all items in the cart."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        return self.items.count()


class CartItem(models.Model):
    """An individual item in the cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} × {self.book.title}"

    def get_subtotal(self):
        return self.book.price * self.quantity

    class Meta:
        unique_together = ('cart', 'book')  # Prevent duplicate cart entries
