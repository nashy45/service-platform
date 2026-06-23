from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProviderProfile


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        user.role = User.ROLE_CUSTOMER
        if commit:
            user.save()
        return user


class ProviderRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    service_area = forms.CharField(max_length=200)
    years_experience = forms.IntegerField(min_value=0)
    hourly_rate = forms.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = User.ROLE_PROVIDER
        if commit:
            user.save()
            ProviderProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio', ''),
                service_area=self.cleaned_data['service_area'],
                years_experience=self.cleaned_data['years_experience'],
                hourly_rate=self.cleaned_data['hourly_rate'],
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'address', 'profile_picture']


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ['bio', 'service_area', 'years_experience', 'hourly_rate', 'is_available', 'id_document']
