from django.contrib import admin
from django.utils import timezone
from .models import Ad, Category, AdImage, PremiumRequest


# Category modeli üçün Admin sinifi
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_tag')
    readonly_fields = ('icon_tag',)

    def icon_tag(self, obj):
        from django.utils.html import format_html
        if obj.icon:
            return format_html('<img src="{}" style="height: 50px; width: 50px; object-fit: cover;" />'.format(obj.icon.url))
        return "Şəkil yoxdur"

    icon_tag.short_description = 'Kateqoriya İkonu'


# Ad modeli üçün Admin sinifi
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'price', 'is_approved', 'is_premium', 'created_at')
    list_filter = ('is_approved', 'is_premium', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'


# AdImage modeli üçün Admin sinifi
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; object-fit: cover;" />'.format(obj.image.url))
        return "Şəkil yoxdur"

    image_tag.short_description = 'Şəkil'


# 🔹 PremiumRequest admin
@admin.register(PremiumRequest)
class PremiumRequestAdmin(admin.ModelAdmin):
    list_display = ("ad", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    actions = ["approve_requests", "reject_requests"]

    def approve_requests(self, request, queryset):
        for req in queryset:
            if req.status == "pending":
                req.status = "approved"
                ad = req.ad
                ad.is_premium = True
                ad.save()
                req.save()
        self.message_user(request, "Seçilmiş elan(lar) premium edildi.")
    approve_requests.short_description = "Seçilmiş elanları Premium et"

    def reject_requests(self, request, queryset):
        queryset.update(status="rejected")
        self.message_user(request, "Seçilmiş sorğular rədd edildi.")
    reject_requests.short_description = "Seçilmiş elanları Rədd et"


# Modelleri admin panelə qeyd edin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(AdImage, AdImageAdmin)
