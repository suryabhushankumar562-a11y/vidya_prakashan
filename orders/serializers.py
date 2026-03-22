from rest_framework import serializers
from .models import Order, OrderItem
from books.serializers import BookListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return str(obj.get_subtotal())


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    final_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_method', 'is_paid',
            'full_name', 'email', 'phone', 'address', 'city', 'state',
            'pincode', 'total_amount', 'discount', 'final_total',
            'items', 'created_at'
        ]
        read_only_fields = ['order_number', 'created_at']

    def get_final_total(self, obj):
        return str(obj.get_final_total())
