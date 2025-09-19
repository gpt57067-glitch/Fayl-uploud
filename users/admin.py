from django.contrib import admin
from .models import UserProfile, Visitor, BlockedIP, BalansArtirma

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "user", "timestamp")

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "reason", "created_at")

# 🔹 Balans artırma admin
@admin.register(BalansArtirma)
class BalansArtirmaAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    actions = ["approve_requests", "reject_requests"]

    def approve_requests(self, request, queryset):
        queryset.update(status="approved")
    approve_requests.short_description = "Seçilmişləri təsdiqlə"

    def reject_requests(self, request, queryset):
        queryset.update(status="rejected")
    reject_requests.short_description = "Seçilmişləri rədd et"
