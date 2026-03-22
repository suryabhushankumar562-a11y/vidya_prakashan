"""
Custom Admin Panel Views for Vidya Prakashan Mandir.
Separate from Django's built-in /admin/ — a branded management interface.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django import forms

from books.models import Book, Category
from orders.models import Order
from accounts.models import UserProfile


def is_staff(user):
    """Check if user is staff/admin."""
    return user.is_authenticated and user.is_staff


staff_required = [login_required, user_passes_test(is_staff, login_url='/accounts/login/')]


# ─── Forms ───────────────────────────────────────────────────────────────────

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'category', 'description', 'price',
            'cover_image', 'pdf_file', 'preview_pages',
            'isbn', 'publisher', 'publication_year', 'language',
            'pages', 'stock', 'is_active', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
            'preview_pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bi-book'}),
        }


# ─── Views ───────────────────────────────────────────────────────────────────

@method_decorator(staff_required, name='dispatch')
class AdminDashboardView(View):
    """Main admin dashboard with stats."""

    def get(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'total_users': User.objects.count(),
            'total_orders': Order.objects.count(),
            'total_revenue': Order.objects.filter(
                status='completed'
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
            'pending_orders': Order.objects.filter(status='pending').count(),
            'active_books': Book.objects.filter(is_active=True).count(),
        }
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
        recent_users = User.objects.order_by('-date_joined')[:5]

        context = {
            'stats': stats,
            'recent_orders': recent_orders,
            'recent_users': recent_users,
        }
        return render(request, 'adminpanel/dashboard.html', context)


# ─── Book Management ─────────────────────────────────────────────────────────

@method_decorator(staff_required, name='dispatch')
class AdminBookListView(View):
    def get(self, request):
        books = Book.objects.select_related('category').all()
        query = request.GET.get('q', '')
        if query:
            books = books.filter(title__icontains=query)
        return render(request, 'adminpanel/book_list.html', {'books': books, 'query': query})


@method_decorator(staff_required, name='dispatch')
class AdminBookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'adminpanel/book_form.html', {'form': form, 'action': 'Add'})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"Book '{book.title}' added successfully!")
            return redirect('admin_book_list')
        return render(request, 'adminpanel/book_form.html', {'form': form, 'action': 'Add'})


@method_decorator(staff_required, name='dispatch')
class AdminBookEditView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'adminpanel/book_form.html', {
            'form': form, 'book': book, 'action': 'Edit'
        })

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{book.title}' updated!")
            return redirect('admin_book_list')
        return render(request, 'adminpanel/book_form.html', {
            'form': form, 'book': book, 'action': 'Edit'
        })


@method_decorator(staff_required, name='dispatch')
class AdminBookDeleteView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        title = book.title
        book.delete()
        messages.success(request, f"Book '{title}' deleted.")
        return redirect('admin_book_list')


# ─── Category Management ─────────────────────────────────────────────────────

@method_decorator(staff_required, name='dispatch')
class AdminCategoryListView(View):
    def get(self, request):
        categories = Category.objects.annotate(book_count=Count('books'))
        return render(request, 'adminpanel/category_list.html', {'categories': categories})


@method_decorator(staff_required, name='dispatch')
class AdminCategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'adminpanel/category_form.html', {'form': form, 'action': 'Add'})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' created!")
            return redirect('admin_category_list')
        return render(request, 'adminpanel/category_form.html', {'form': form, 'action': 'Add'})


@method_decorator(staff_required, name='dispatch')
class AdminCategoryEditView(View):
    def get(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=cat)
        return render(request, 'adminpanel/category_form.html', {'form': form, 'cat': cat, 'action': 'Edit'})

    def post(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{cat.name}' updated!")
            return redirect('admin_category_list')
        return render(request, 'adminpanel/category_form.html', {'form': form, 'cat': cat, 'action': 'Edit'})


@method_decorator(staff_required, name='dispatch')
class AdminCategoryDeleteView(View):
    def post(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        name = cat.name
        cat.delete()
        messages.success(request, f"Category '{name}' deleted.")
        return redirect('admin_category_list')


# ─── User Management ─────────────────────────────────────────────────────────

@method_decorator(staff_required, name='dispatch')
class AdminUserListView(View):
    def get(self, request):
        users = User.objects.select_related('profile').order_by('-date_joined')
        return render(request, 'adminpanel/user_list.html', {'users': users})


# ─── Order Management ────────────────────────────────────────────────────────

@method_decorator(staff_required, name='dispatch')
class AdminOrderListView(View):
    def get(self, request):
        orders = Order.objects.select_related('user').all()
        status_filter = request.GET.get('status', '')
        if status_filter:
            orders = orders.filter(status=status_filter)
        return render(request, 'adminpanel/order_list.html', {
            'orders': orders,
            'status_filter': status_filter
        })


@method_decorator(staff_required, name='dispatch')
class AdminOrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'adminpanel/order_detail.html', {'order': order})

    def post(self, request, pk):
        """Update order status."""
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'completed', 'cancelled']:
            order.status = new_status
            if new_status == 'completed':
                order.is_paid = True
            order.save()
            messages.success(request, f"Order #{order.order_number} status updated to '{new_status}'.")
        return redirect('admin_order_detail', pk=pk)
