from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User, ProviderProfile
from bookings.models import Booking


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.customer.email} - {self.rating} stars"
