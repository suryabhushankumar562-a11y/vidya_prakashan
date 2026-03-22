"""
Orders Models — Order and OrderItem track purchases.
"""

from django.db import models
from django.contrib.auth.models import User
from books.models import Book
import uuid


class Order(models.Model):
    """
    A placed order. Status moves: pending → completed (or cancelled).
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
        ('upi', 'UPI'),
    ]

    order_number = models.CharField(
        max_length=20, unique=True, blank=True,
        help_text="Auto-generated unique order number"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    is_paid = models.BooleanField(default=False)

    # Delivery information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate order number like VP-2024-A3F9
        if not self.order_number:
            self.order_number = f"VP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"

    def get_final_total(self):
        return self.total_amount - self.discount

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """A single book within an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Snapshot price at time of purchase

    def __str__(self):
        return f"{self.quantity} × {self.book.title if self.book else 'Deleted Book'}"

    def get_subtotal(self):
        return self.price * self.quantity
