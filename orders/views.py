"""
Orders Views — Checkout, Order Confirmation, Order History, Order Detail
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Order, OrderItem
from cart.models import Cart, CartItem


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    """Checkout page — collects delivery info and confirms order."""

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.items.select_related('book').all()
        except Cart.DoesNotExist:
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        if not items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        # Pre-fill form with user's existing info
        profile = getattr(request.user, 'profile', None)
        context = {
            'cart': cart,
            'items': items,
            'total': cart.get_total(),
            'profile': profile,
        }
        return render(request, 'orders/checkout.html', context)

    def post(self, request):
        """Place the order."""
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.items.select_related('book').all()
        except Cart.DoesNotExist:
            return redirect('cart')

        if not items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        # Collect delivery info from form
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name', request.user.get_full_name()),
            email=request.POST.get('email', request.user.email),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            pincode=request.POST.get('pincode', ''),
            payment_method=request.POST.get('payment_method', 'cod'),
            total_amount=cart.get_total(),
        )

        # Move cart items → order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,  # Snapshot current price
            )

        # Mark order as completed (COD / simple flow)
        if order.payment_method == 'cod':
            order.status = 'completed'
            order.save()

        # Clear the cart
        cart.items.all().delete()

        messages.success(
            request,
            f"🎉 Order #{order.order_number} placed successfully!"
        )
        return redirect('order_confirmation', order_number=order.order_number)


@method_decorator(login_required, name='dispatch')
class OrderConfirmationView(View):
    """Show order confirmation after successful checkout."""

    def get(self, request, order_number):
        order = get_object_or_404(
            Order, order_number=order_number, user=request.user
        )
        return render(request, 'orders/order_confirmation.html', {'order': order})


@method_decorator(login_required, name='dispatch')
class OrderHistoryView(View):
    """List all orders for the logged-in user."""

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders/order_history.html', {'orders': orders})


@method_decorator(login_required, name='dispatch')
class OrderDetailView(View):
    """Full detail of a single order."""

    def get(self, request, order_number):
        order = get_object_or_404(
            Order, order_number=order_number, user=request.user
        )
        return render(request, 'orders/order_detail.html', {'order': order})
