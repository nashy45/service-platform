from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from bookings.models import Booking


@login_required
def leave_review(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user, status='completed')

    if hasattr(booking, 'review'):
        messages.info(request, 'You already reviewed this booking.')
        return redirect('booking_detail', pk=booking_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        Review.objects.create(
            booking=booking,
            customer=request.user,
            provider=booking.provider,
            rating=rating,
            comment=comment,
        )
        # Update provider average rating
        provider = booking.provider
        reviews = provider.reviews_received.all()
        provider.rating = sum(r.rating for r in reviews) / reviews.count()
        provider.save()
        messages.success(request, 'Review submitted. Thank you!')
        return redirect('booking_detail', pk=booking_id)

    return render(request, 'reviews/leave_review.html', {'booking': booking})
