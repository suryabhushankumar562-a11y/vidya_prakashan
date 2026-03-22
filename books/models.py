"""
Books Models — Category, Book, Review
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """
    Book categories (e.g., Science, Mathematics, History, Computer Science).
    Uses slug for clean URLs like /category/science/
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="Bootstrap Icons class name, e.g. bi-book"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_book_count(self):
        return self.books.filter(is_active=True).count()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']


class Book(models.Model):
    """
    Main Book model — stores all book information including cover image and PDF.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='books'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # File uploads
    cover_image = models.ImageField(
        upload_to='book_covers/', blank=True, null=True,
        help_text="Book cover image (JPEG/PNG)"
    )
    pdf_file = models.FileField(
        upload_to='book_pdfs/',
        blank=True, null=True,
        help_text="Full PDF of the book"
    )
    preview_pages = models.IntegerField(
        default=10,
        help_text="Number of preview pages available to non-purchasers"
    )

    # Metadata
    isbn = models.CharField(max_length=20, blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, default='Hindi/English')
    pages = models.IntegerField(blank=True, null=True)

    # Status flags
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage featured section"
    )
    stock = models.IntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def get_review_count(self):
        return self.reviews.count()

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    """User reviews and ratings for books."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}★)"

    class Meta:
        unique_together = ('book', 'user')  # One review per user per book
        ordering = ['-created_at']
