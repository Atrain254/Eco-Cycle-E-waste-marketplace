from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Item

# Your existing ItemForm
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'title', 'image', 'description', 'condition'] 
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# NEW: The Registration Form
class UserRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('household', 'Household / Citizen'),
        ('technician', 'Jua Kali Technician'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect, help_text="Are you disposing of waste, or looking for parts?")
    phone_number = forms.CharField(max_length=15, required=False, help_text="Optional: For MPESA or contact purposes.")

    class Meta:
        model = User
        # We ask for a username and email. (UserCreationForm automatically handles passwords!)
        fields = ['username', 'email']