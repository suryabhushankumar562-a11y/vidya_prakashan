"""
Books context processor — injects nav_categories into every template.
Used by the navbar dropdown to show category links globally.
"""

from .models import Category


def nav_categories(request):
    """Return top 8 categories for the navbar dropdown."""
    categories = Category.objects.all()[:8]
    return {'nav_categories': categories}
