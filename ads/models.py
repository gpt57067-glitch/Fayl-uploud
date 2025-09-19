from django.db import models
from django.contrib.auth.models import User


# Kateqoriya modeli
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    def __str__(self):
        return self.name


# Elan modeli
class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)  # <- əlavə et
    is_approved = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)  # 🔹 Premium elan üçün
    created_at = models.DateTimeField(auto_now_add=True)
    premium_date = models.DateTimeField(blank=True, null=True)  # 🔹 Təsdiqləndiyi vaxt
    premium_until = models.DateTimeField(blank=True, null=True)  # 🔹 Bitmə tarixi

    def __str__(self):
        return self.title


# Elan şəkilləri modeli
class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ad_images/')

    def __str__(self):
        return f"Image for {self.ad.title}"


# 🔹 Premium elan sorğuları
class PremiumRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", "Gözləmədə"),
        ("approved", "Təsdiqlənib"),
        ("rejected", "Rədd edilib"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="premium_requests")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="premium_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad.title} - {self.user.username} - {self.status}"
