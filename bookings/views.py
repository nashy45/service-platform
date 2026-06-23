from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from services.models import Service


@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    if not request.user.is_customer():
        messages.error(request, 'Only customers can make bookings.')
        return redirect('service_detail', pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.provider = service.provider
            booking.service = service
            booking.total_price = service.price
            booking.save()
            messages.success(request, 'Booking created! Awaiting provider confirmation.')
            return redirect('booking_detail', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form, 'service': service})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.customer != request.user and booking.provider.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    if request.user.is_customer():
        bookings = Booking.objects.filter(customer=request.user)
    elif request.user.is_provider():
        bookings = Booking.objects.filter(provider=request.user.provider_profile)
    else:
        bookings = Booking.objects.none()
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def update_booking_status(request, pk, status):
    if request.method != 'POST':
        return redirect('booking_detail', pk=pk)
    booking = get_object_or_404(Booking, pk=pk)
    allowed = {
        'confirmed': request.user.is_provider() and booking.provider.user == request.user,
        'cancelled': booking.customer == request.user or booking.provider.user == request.user,
        'in_progress': request.user.is_provider() and booking.provider.user == request.user,
        'completed': request.user.is_provider() and booking.provider.user == request.user,
    }
    if allowed.get(status):
        booking.status = status
        booking.save()
        messages.success(request, f'Booking marked as {status}.')
    else:
        messages.error(request, 'Action not allowed.')
    return redirect('booking_detail', pk=pk)
