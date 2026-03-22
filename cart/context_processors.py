"""
Cart context processor — injects cart_count into every template.
This allows the navbar to always show the current cart item count.
"""

from .models import Cart


def cart_count(request):
    """Return the number of items in the user's cart."""
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_item_count()
        except Cart.DoesNotExist:
            count = 0
    return {'cart_count': count}
