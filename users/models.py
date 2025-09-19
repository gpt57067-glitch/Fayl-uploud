from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)  # <-- BU ƏLAVƏ OLUB

    def __str__(self):
        return self.user.username


class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


class BalansArtirma(models.Model):
    STATUS_CHOICES = (
        ("pending", "Gözləmədə"),
        ("approved", "Təsdiqlənib"),
        ("rejected", "Rədd edilib"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="balans_sorğulari")
    screenshot = models.ImageField(upload_to="balans_screenshots/")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:  # mövcud obyekt yenilənirsə
            old = BalansArtirma.objects.get(pk=self.pk)
            if old.status != "approved" and self.status == "approved":
                profile, created = UserProfile.objects.get_or_create(user=self.user)
                profile.balance += self.amount
                profile.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} AZN - {self.status}"


