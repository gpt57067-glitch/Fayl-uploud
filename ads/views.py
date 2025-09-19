from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Ad, Category, AdImage, PremiumRequest
from .forms import AdForm
from users.models import UserProfile  # balans üçün istifadəçi profili
import re  # <-- re modulunu import edin



@login_required
def ad_create(request):
    """Yeni elan yaratmaq üçün funksiya."""
    if request.method == 'POST':
        form = AdForm(request.POST)
        files = request.FILES.getlist('images')  # Şəkilləri əldə edin
        video_url = models.URLField(blank=True, null=True)


        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()

            for f in files:
                AdImage.objects.create(ad=ad, image=f)

            return redirect('users:home')
    else:
        form = AdForm()
    return render(request, 'ads/ad_create.html', {'form': form})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form})


@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('users:profile')
    return render(request, 'ads/delete_ad.html', {'ad': ad})


def search_results(request):
    query = request.GET.get('q')
    ads = Ad.objects.filter(is_approved=True).order_by("-is_premium", "-created_at")

    if query:
        ads = ads.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'ads/search_results.html', {'ads': ads, 'query': query})


def ad_list_by_category(request, category_name):
    """Kateqoriya adına görə elanları süzən funksiya."""
    category = get_object_or_404(Category, name=category_name)
    ads = Ad.objects.filter(category=category, is_approved=True).order_by("-is_premium", "-created_at")
    
    context = {
        'category': category,
        'ads': ads
    }
    return render(request, 'ads/ad_list_by_category.html', context)


# 🔹 Premium elan funksiyası
@login_required
def make_premium(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)

    # balans yoxla
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if not hasattr(profile, "balance"):
        profile.balance = 0

    if profile.balance < 3:
        messages.error(request, "❌ Balansınızda kifayət qədər məbləğ yoxdur.")
        return redirect("ads:ad_detail", pk=ad.id)

    # balansdan çıx
    profile.balance -= 3
    profile.save()

    # Premium sorğu yarat
    PremiumRequest.objects.create(
        user=request.user,
        ad=ad,
        status="pending"
    )

    messages.success(request, "✅ Premium sorğunuz göndərildi. Admin təsdiq etməlidir.")
    return redirect("ads:ad_detail", pk=ad.id)
