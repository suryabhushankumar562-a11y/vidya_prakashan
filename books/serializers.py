"""
Books Serializers for the REST API.
"""

from rest_framework import serializers
from .models import Category, Book, Review


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'book_count']

    def get_book_count(self, obj):
        return obj.get_book_count()


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'category_name',
            'price', 'cover_image', 'avg_rating', 'is_featured'
        ]

    def get_avg_rating(self, obj):
        return obj.get_average_rating()


class BookDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views."""
    category = CategorySerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'category',
            'description', 'price', 'cover_image', 'isbn',
            'publisher', 'publication_year', 'language', 'pages',
            'is_featured', 'preview_pages', 'avg_rating',
            'review_count', 'reviews', 'created_at'
        ]

    def get_avg_rating(self, obj):
        return obj.get_average_rating()

    def get_review_count(self, obj):
        return obj.get_review_count()
