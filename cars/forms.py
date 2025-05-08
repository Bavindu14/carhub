from django import forms
from .models import Contact, Car, CarImage

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['owner', 'created_date', 'is_sold']
        widgets = {
            'features': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 6}),
        }

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']

CarImageFormSet = forms.inlineformset_factory(
    Car, CarImage, form=CarImageForm, extra=4, can_delete=True
)