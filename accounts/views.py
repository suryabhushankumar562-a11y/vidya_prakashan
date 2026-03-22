"""
Accounts Views — Registration, Login, Logout, Dashboard
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from .forms import RegisterForm, LoginForm, UserProfileForm
from .models import UserProfile
from orders.models import Order


class RegisterView(View):
    """Handle user registration — GET shows form, POST processes it."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create the user but don't save yet
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create the linked UserProfile
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', '')
            )

            # Auto-login after registration
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
            return redirect('dashboard')

        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    """Handle user login."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            # Redirect to 'next' parameter if present, else dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)

        messages.error(request, "Invalid username or password.")
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    """Log the user out and redirect home."""

    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('home')


class DashboardView(View):
    """User dashboard — shows profile, orders, purchased books."""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        # Get or create profile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        # Get recent orders
        recent_orders = Order.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]

        context = {
            'profile': profile,
            'recent_orders': recent_orders,
        }
        return render(request, 'accounts/dashboard.html', context)

    def post(self, request):
        """Handle profile update form submission."""
        if not request.user.is_authenticated:
            return redirect('login')

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Error updating profile.")

        return redirect('dashboard')
