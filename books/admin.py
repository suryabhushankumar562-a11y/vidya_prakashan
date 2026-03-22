"""
Books Admin registration.
"""

from django.contrib import admin
from .models import Category, Book, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_book_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['title', 'author', 'isbn']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active', 'is_featured', 'price']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating']
