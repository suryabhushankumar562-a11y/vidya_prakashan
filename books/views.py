"""
Books Views — Homepage, Book Listing, Book Detail, Categories, Search, PDF Viewer
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import FileResponse, HttpResponseForbidden, Http404
from django.db.models import Q
import os

from .models import Book, Category, Review
from orders.models import Order, OrderItem


class HomeView(View):
    """Homepage with featured books and category showcase."""

    def get(self, request):
        featured_books = Book.objects.filter(
            is_active=True, is_featured=True
        )[:8]
        latest_books = Book.objects.filter(is_active=True)[:6]
        categories = Category.objects.all()[:8]

        context = {
            'featured_books': featured_books,
            'latest_books': latest_books,
            'categories': categories,
        }
        return render(request, 'home.html', context)


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class BookListView(View):
    """Paginated book listing with search and category filter."""

    def get(self, request):
        books = Book.objects.filter(is_active=True)
        categories = Category.objects.all()

        # Search by title or author
        query = request.GET.get('q', '').strip()
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )

        # Filter by category slug
        category_slug = request.GET.get('category', '')
        selected_category = None
        if category_slug:
            selected_category = get_object_or_404(Category, slug=category_slug)
            books = books.filter(category=selected_category)

        # Filter by price range
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        if min_price:
            books = books.filter(price__gte=min_price)
        if max_price:
            books = books.filter(price__lte=max_price)

        context = {
            'books': books,
            'categories': categories,
            'query': query,
            'selected_category': selected_category,
            'min_price': min_price,
            'max_price': max_price,
        }
        return render(request, 'books/book_list.html', context)


class BookDetailView(View):
    """Full detail page for a single book."""

    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug, is_active=True)
        reviews = book.reviews.all()

        # Check if logged-in user has purchased this book
        has_purchased = False
        user_review = None
        if request.user.is_authenticated:
            has_purchased = OrderItem.objects.filter(
                order__user=request.user,
                order__status='completed',
                book=book
            ).exists()
            user_review = Review.objects.filter(
                book=book, user=request.user
            ).first()

        # Related books in same category
        related_books = Book.objects.filter(
            category=book.category, is_active=True
        ).exclude(id=book.id)[:4]

        context = {
            'book': book,
            'reviews': reviews,
            'has_purchased': has_purchased,
            'user_review': user_review,
            'related_books': related_books,
            'avg_rating': book.get_average_rating(),
        }
        return render(request, 'books/book_detail.html', context)

    def post(self, request, slug):
        """Handle review submission."""
        if not request.user.is_authenticated:
            return redirect('login')

        book = get_object_or_404(Book, slug=slug)

        # Check if user already reviewed this book
        existing = Review.objects.filter(book=book, user=request.user).first()
        if existing:
            existing.rating = request.POST.get('rating', existing.rating)
            existing.comment = request.POST.get('comment', existing.comment)
            existing.save()
        else:
            Review.objects.create(
                book=book,
                user=request.user,
                rating=request.POST.get('rating', 5),
                comment=request.POST.get('comment', '')
            )

        return redirect('book_detail', slug=slug)


class CategoryListView(View):
    """Page listing all categories."""

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'books/category_list.html', {'categories': categories})


class CategoryBooksView(View):
    """Page showing all books in a given category."""

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        books = Book.objects.filter(category=category, is_active=True)

        # Search within category
        query = request.GET.get('q', '').strip()
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )

        context = {
            'category': category,
            'books': books,
            'query': query,
        }
        return render(request, 'books/category_books.html', context)


class PDFViewerView(View):
    """
    Secure PDF viewing.
    - Preview (limited pages) available to all users.
    - Full PDF only for authenticated users who have purchased the book.
    - Direct file access is blocked; served through Django.
    """

    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug, is_active=True)

        if not book.pdf_file:
            raise Http404("No PDF available for this book.")

        # Check if user has purchased this book
        has_purchased = False
        if request.user.is_authenticated:
            has_purchased = OrderItem.objects.filter(
                order__user=request.user,
                order__status='completed',
                book=book
            ).exists()

        context = {
            'book': book,
            'has_purchased': has_purchased,
        }
        return render(request, 'books/pdf_viewer.html', context)


class PDFServeView(View):
    """
    Serves the actual PDF file securely.
    Only authenticated + purchased users get the full file.
    Others get a 403 Forbidden response.
    """

    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug, is_active=True)

        if not book.pdf_file:
            raise Http404("PDF not found.")

        # Must be logged in
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Login required to access this PDF.")

        # Must have purchased (or be staff/superuser)
        if not request.user.is_staff:
            has_purchased = OrderItem.objects.filter(
                order__user=request.user,
                order__status='completed',
                book=book
            ).exists()
            if not has_purchased:
                return HttpResponseForbidden("Purchase this book to access the full PDF.")

        # Serve the file
        response = FileResponse(
            open(book.pdf_file.path, 'rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(book.pdf_file.name)}"'
        return response
