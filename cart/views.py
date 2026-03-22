"""
Cart Views — Add, Remove, Update, and View Cart
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.http import JsonResponse

from .models import Cart, CartItem
from books.models import Book


def get_or_create_cart(user):
    """Helper: get or create cart for a user."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@method_decorator(login_required, name='dispatch')
class CartView(View):
    """Display the user's cart."""

    def get(self, request):
        cart = get_or_create_cart(request.user)
        items = cart.items.select_related('book').all()
        context = {
            'cart': cart,
            'items': items,
            'total': cart.get_total(),
        }
        return render(request, 'cart/cart.html', context)


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    """Add a book to the cart, or increment quantity."""

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id, is_active=True)
        cart = get_or_create_cart(request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, book=book,
            defaults={'quantity': 1}
        )

        if not created:
            # Book already in cart — increment quantity
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"'{book.title}' quantity updated in cart.")
        else:
            messages.success(request, f"'{book.title}' added to cart!")

        # Support AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.get_item_count(),
                'message': 'Added to cart!'
            })

        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    """Remove a book from the cart."""

    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        title = item.book.title
        item.delete()
        messages.success(request, f"'{title}' removed from cart.")
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class UpdateCartView(View):
    """Update quantity of a cart item."""

    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            item.delete()
            messages.success(request, "Item removed from cart.")
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, "Cart updated.")

        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class ClearCartView(View):
    """Remove all items from the cart."""

    def post(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        messages.success(request, "Cart cleared.")
        return redirect('cart')
