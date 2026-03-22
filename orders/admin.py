from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'payment_method', 'created_at', 'is_paid']
    list_filter = ['status', 'payment_method', 'is_paid']
    search_fields = ['order_number', 'user__username', 'full_name']
    list_editable = ['status', 'is_paid']
    inlines = [OrderItemInline]
