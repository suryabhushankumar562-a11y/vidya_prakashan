"""
REST API Views using Django REST Framework.
Provides JSON endpoints for authentication, books, categories, cart, and orders.
"""

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer, UserSerializer
from books.models import Book, Category
from books.serializers import BookListSerializer, BookDetailSerializer, CategorySerializer
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from orders.models import Order
from orders.serializers import OrderSerializer


# ─── Auth API ────────────────────────────────────────────────────────────────

class RegisterAPIView(APIView):
    """
    POST /api/auth/register/
    Register a new user and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT tokens for instant login
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Registration successful!',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    """
    GET /api/auth/me/
    Returns current authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ─── Books API ────────────────────────────────────────────────────────────────

class BookListAPIView(generics.ListAPIView):
    """
    GET /api/books/
    Returns paginated list of active books.
    Supports ?q=search and ?category=slug filters.
    """
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True)
        q = self.request.query_params.get('q', '')
        category = self.request.query_params.get('category', '')
        featured = self.request.query_params.get('featured', '')

        if q:
            queryset = queryset.filter(title__icontains=q)
        if category:
            queryset = queryset.filter(category__slug=category)
        if featured:
            queryset = queryset.filter(is_featured=True)

        return queryset


class BookDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/books/<slug>/
    Returns full detail for a single book.
    """
    serializer_class = BookDetailSerializer
    permission_classes = [AllowAny]
    queryset = Book.objects.filter(is_active=True)
    lookup_field = 'slug'


# ─── Categories API ───────────────────────────────────────────────────────────

class CategoryListAPIView(generics.ListAPIView):
    """
    GET /api/categories/
    Returns all categories with book counts.
    """
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()


class CategoryBooksAPIView(APIView):
    """
    GET /api/categories/<slug>/books/
    Returns all books in a given category.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        books = Book.objects.filter(category=category, is_active=True)
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response({
            'category': CategorySerializer(category).data,
            'books': serializer.data
        })


# ─── Cart API ─────────────────────────────────────────────────────────────────

class CartAPIView(APIView):
    """
    GET  /api/cart/        — View current cart
    POST /api/cart/        — Add item to cart  {book_id, quantity}
    DELETE /api/cart/<id>/ — Remove item from cart
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        book = get_object_or_404(Book, id=book_id, is_active=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, book=book,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response({
            'message': 'Added to cart',
            'cart_count': cart.get_item_count()
        }, status=status.HTTP_201_CREATED)


class CartItemDeleteAPIView(APIView):
    """DELETE /api/cart/<item_id>/"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)


# ─── Orders API ───────────────────────────────────────────────────────────────

class OrderListAPIView(APIView):
    """
    GET  /api/orders/ — List user's orders
    POST /api/orders/ — Place a new order from current cart
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Place order from cart via API."""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        items = cart.items.all()
        if not items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=request.user,
            full_name=request.data.get('full_name', request.user.get_full_name()),
            email=request.data.get('email', request.user.email),
            phone=request.data.get('phone', ''),
            address=request.data.get('address', ''),
            city=request.data.get('city', ''),
            state=request.data.get('state', ''),
            pincode=request.data.get('pincode', ''),
            payment_method=request.data.get('payment_method', 'cod'),
            total_amount=cart.get_total(),
            status='completed',
        )

        from orders.models import OrderItem
        for item in items:
            OrderItem.objects.create(
                order=order, book=item.book,
                quantity=item.quantity, price=item.book.price
            )

        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(generics.RetrieveAPIView):
    """GET /api/orders/<order_number>/"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_number'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# ─── Secure PDF API ───────────────────────────────────────────────────────────

class PDFAccessAPIView(APIView):
    """
    GET /api/books/<slug>/pdf-access/
    Returns whether the current user can access the full PDF.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        book = get_object_or_404(Book, slug=slug, is_active=True)

        from orders.models import OrderItem
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status='completed',
            book=book
        ).exists()

        return Response({
            'book_slug': slug,
            'has_pdf': bool(book.pdf_file),
            'has_purchased': has_purchased or request.user.is_staff,
            'pdf_url': request.build_absolute_uri(f'/books/{slug}/pdf/') if (has_purchased or request.user.is_staff) else None,
        })
