from django import forms
from .models import Service, ServiceCategory


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'price', 'price_type', 'duration_hours']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ServiceCategory.objects.filter(is_active=True)

        base_class = (
            'w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white'
        )
        for name, field in self.fields.items():
            field.widget.attrs['class'] = base_class
            field.widget.attrs.pop('required', None)  # let Django handle validation
