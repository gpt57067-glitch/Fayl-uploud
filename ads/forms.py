from django import forms
from .models import Ad


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AdForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Ad
        fields = [
            'title',
            'description',
            'category',
            'price',
            'location',
            'phone_number',
            'email',
            'video_url',  # 🔹 Video link sahəsini əlavə etdik
            'images'
        ]
