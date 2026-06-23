from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, ProviderRegistrationForm, UserProfileForm, ProviderProfileForm
from .models import User


def home(request):
    from services.models import ServiceCategory
    from accounts.models import ProviderProfile
    from bookings.models import Booking
    from reviews.models import Review
    from django.db.models import Avg

    categories = ServiceCategory.objects.filter(is_active=True)

    # Real stats
    total_providers = ProviderProfile.objects.filter(status='approved').count()
    total_bookings = Booking.objects.count()
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    default_services = [
        {'name': 'Driver Booking', 'icon': 'fa-solid fa-car'},
        {'name': 'House Cleaning', 'icon': 'fa-solid fa-broom'},
        {'name': 'Daycare', 'icon': 'fa-solid fa-baby'},
        {'name': 'Office Cleaning', 'icon': 'fa-solid fa-building'},
        {'name': 'Personal Chef', 'icon': 'fa-solid fa-utensils'},
        {'name': 'Plumbing', 'icon': 'fa-solid fa-wrench'},
        {'name': 'Electrician', 'icon': 'fa-solid fa-bolt'},
        {'name': 'Tutoring', 'icon': 'fa-solid fa-book-open'},
        {'name': 'Elderly Care', 'icon': 'fa-solid fa-heart-pulse'},
        {'name': 'Laundry', 'icon': 'fa-solid fa-shirt'},
        {'name': 'Gardening', 'icon': 'fa-solid fa-leaf'},
        {'name': 'Security', 'icon': 'fa-solid fa-shield-halved'},
    ]
    return render(request, 'home.html', {
        'categories': categories,
        'default_services': default_services,
        'total_providers': total_providers,
        'total_bookings': total_bookings,
        'avg_rating': avg_rating,
    })


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register_customer.html', {'form': form})


def register_provider(request):
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Provider account created! Awaiting approval.')
            return redirect('dashboard')
    else:
        form = ProviderRegistrationForm()
    return render(request, 'accounts/register_provider.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            if user_obj.check_password(password):
                login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def toggle_availability(request):
    """Provider toggles their availability on/off."""
    if request.method == 'POST' and request.user.is_provider():
        profile = request.user.provider_profile
        profile.is_available = not profile.is_available
        profile.save()
    return redirect('dashboard')


def reset_password_request(request):
    """Step 1 — user enters their email."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user_obj = User.objects.get(email=email)
            return redirect('reset_password_set', user_id=user_obj.pk)
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
    return render(request, 'accounts/reset_password_request.html')


def reset_password_set(request, user_id):
    """Step 2 — user sets a new password directly."""
    user_obj = User.objects.filter(pk=user_id).first()
    if not user_obj:
        messages.error(request, 'Invalid request.')
        return redirect('reset_password_request')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password reset successfully! You can now log in.')
            return redirect('login')

    return render(request, 'accounts/reset_password_set.html', {'reset_user': user_obj})


@login_required
def dashboard(request):
    user = request.user
    if user.is_customer():
        from bookings.models import Booking as B
        total = B.objects.filter(customer=user).count()
        completed = B.objects.filter(customer=user, status='completed').count()
        pending = B.objects.filter(customer=user, status='pending').count()
        confirmed = B.objects.filter(customer=user, status='confirmed').count()
        bookings = B.objects.filter(customer=user).order_by('-created_at')[:6]
        return render(request, 'accounts/dashboard_customer.html', {
            'bookings': bookings,
            'total': total,
            'completed': completed,
            'pending': pending,
            'confirmed': confirmed,
        })
    elif user.is_provider():
        from bookings.models import Booking as B
        profile = user.provider_profile
        total = B.objects.filter(provider=profile).count()
        completed = B.objects.filter(provider=profile, status='completed').count()
        pending = B.objects.filter(provider=profile, status='pending').count()
        in_progress = B.objects.filter(provider=profile, status='in_progress').count()
        bookings = B.objects.filter(provider=profile).order_by('-created_at')[:6]
        return render(request, 'accounts/dashboard_provider.html', {
            'bookings': bookings,
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'profile': profile,
        })
    else:
        return redirect('admin_dashboard')


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=user)

    provider_form = None
    if user.is_provider() and hasattr(user, 'provider_profile'):
        if request.method == 'POST':
            provider_form = ProviderProfileForm(request.POST, request.FILES, instance=user.provider_profile)
            if provider_form.is_valid():
                provider_form.save()
        else:
            provider_form = ProviderProfileForm(instance=user.provider_profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'provider_form': provider_form,
    })


# ── Admin views ──────────────────────────────────────────────────────────────

def admin_required(view_func):
    """Decorator: login required + must be admin role."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    from bookings.models import Booking
    from accounts.models import ProviderProfile
    from services.models import Service

    total_users = User.objects.count()
    total_customers = User.objects.filter(role='customer').count()
    total_providers = ProviderProfile.objects.count()
    pending_providers = ProviderProfile.objects.filter(status='pending').count()
    total_bookings = Booking.objects.count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_services = Service.objects.filter(is_active=True).count()

    pending_provider_list = ProviderProfile.objects.filter(status='pending').select_related('user')[:5]
    recent_bookings = Booking.objects.select_related('service', 'customer', 'provider__user').order_by('-created_at')[:8]
    recent_users = User.objects.order_by('-created_at')[:8]

    return render(request, 'accounts/dashboard_admin.html', {
        'total_users': total_users,
        'total_customers': total_customers,
        'total_providers': total_providers,
        'pending_providers': pending_providers,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'pending_bookings': pending_bookings,
        'total_services': total_services,
        'pending_provider_list': pending_provider_list,
        'recent_bookings': recent_bookings,
        'recent_users': recent_users,
    })


@admin_required
def admin_users(request):
    users = User.objects.order_by('-created_at')
    return render(request, 'accounts/admin_users.html', {'users': users})


@admin_required
def admin_providers(request):
    from accounts.models import ProviderProfile
    providers = ProviderProfile.objects.select_related('user').order_by('-created_at')
    return render(request, 'accounts/admin_providers.html', {'providers': providers})


@admin_required
def admin_bookings(request):
    from bookings.models import Booking
    bookings = Booking.objects.select_related('service', 'customer', 'provider__user').order_by('-created_at')
    return render(request, 'accounts/admin_bookings.html', {'bookings': bookings})


@admin_required
def admin_approve_provider(request, pk, status):
    from accounts.models import ProviderProfile
    provider = ProviderProfile.objects.get(pk=pk)
    if status in ('approved', 'rejected', 'pending'):
        provider.status = status
        provider.save()
        messages.success(request, f'Provider {provider.user.get_full_name()} marked as {status}.')
    return redirect('admin_providers')
