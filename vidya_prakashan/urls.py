"""
Main URL Configuration for Vidya Prakashan Mandir
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from books.views import HomeView, AboutView

urlpatterns = [
    # Django built-in admin
    path('django-admin/', admin.site.urls),

    # Homepage & About
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),

    # Accounts (register, login, logout, dashboard)
    path('accounts/', include('accounts.urls')),

    # Books (listing, detail, categories, search)
    path('books/', include('books.urls')),

    # Cart
    path('cart/', include('cart.urls')),

    # Orders
    path('orders/', include('orders.urls')),

    # Custom Admin Panel
    path('adminpanel/', include('adminpanel.urls')),

    # REST API (DRF)
    path('api/', include('api.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
