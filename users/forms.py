from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import BalansArtirma

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # 'username' sahəsini aradan qaldırırıq
    username = None 
    
    # 'email' sahəsini tələb olunan edirik
    email = forms.EmailField(
        required=True,
        label="E-Poçt",
        help_text="E-poçt ünvanınızı daxil edin"
    )
    
    # 'phone_number' sahəsini əlavə edirik
    phone_number = forms.CharField(max_length=20, required=True, help_text="Telefon nömrənizi daxil edin")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    # 'username' sahəsinin yerinə 'email' qoyuruq
    username = forms.CharField(
        label="E-Poçt",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )


# 🔹 Balans artırma formu
class BalansArtirmaForm(forms.ModelForm):
    class Meta:
        model = BalansArtirma
        fields = ["amount", "screenshot"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Məbləği daxil edin"}),
            "screenshot": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
