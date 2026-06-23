from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceCategory, Service
from .forms import ServiceForm
from accounts.models import ProviderProfile


def category_list(request):
    categories = ServiceCategory.objects.filter(is_active=True)
    return render(request, 'services/category_list.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    services = Service.objects.filter(category=category, is_active=True,
                                      provider__status='approved')
    return render(request, 'services/category_detail.html', {
        'category': category,
        'services': services,
    })


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    reviews = service.provider.reviews_received.all().order_by('-created_at')[:10]
    return render(request, 'services/service_detail.html', {
        'service': service,
        'reviews': reviews,
    })


def provider_list(request):
    providers = ProviderProfile.objects.filter(status='approved', is_available=True)
    category_slug = request.GET.get('category')
    if category_slug:
        providers = providers.filter(services__category__slug=category_slug).distinct()
    return render(request, 'services/provider_list.html', {'providers': providers})


def provider_detail(request, pk):
    provider = get_object_or_404(ProviderProfile, pk=pk, status='approved')
    services = provider.services.filter(is_active=True)
    reviews = provider.reviews_received.all().order_by('-created_at')
    return render(request, 'services/provider_detail.html', {
        'provider': provider,
        'services': services,
        'reviews': reviews,
    })


@login_required
def my_services(request):
    """Provider's own service listing page."""
    if not request.user.is_provider():
        messages.error(request, 'Only providers can manage services.')
        return redirect('dashboard')
    services = Service.objects.filter(provider=request.user.provider_profile)
    return render(request, 'services/my_services.html', {'services': services})


@login_required
def add_service(request):
    """Provider adds a new service."""
    if not request.user.is_provider():
        messages.error(request, 'Only providers can add services.')
        return redirect('dashboard')
    if request.user.provider_profile.status != 'approved':
        messages.error(request, 'Your account must be approved before adding services.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user.provider_profile
            service.save()
            messages.success(request, f'"{service.title}" added successfully!')
            return redirect('my_services')
    else:
        form = ServiceForm()
    return render(request, 'services/add_service.html', {'form': form})


@login_required
def edit_service(request, pk):
    """Provider edits their service."""
    service = get_object_or_404(Service, pk=pk, provider=request.user.provider_profile)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated.')
            return redirect('my_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/add_service.html', {'form': form, 'editing': True, 'service': service})


@login_required
def delete_service(request, pk):
    """Provider deletes their service."""
    service = get_object_or_404(Service, pk=pk, provider=request.user.provider_profile)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
    return redirect('my_services')
