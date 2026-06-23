from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    booking_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'location', 'notes']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Enter service location'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special instructions?'}),
        }
