from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from ads.models import Category, Ad
from .forms import CustomUserCreationForm, CustomAuthenticationForm, BalansArtirmaForm
from .models import UserProfile, BalansArtirma

def home(request):
    categories = Category.objects.all()

    # Premium elanlar birinci
    premium_ads = Ad.objects.filter(is_approved=True, is_premium=True).order_by('-created_at')

    # Normal elanlar
    normal_ads = Ad.objects.filter(is_approved=True, is_premium=False).order_by('-created_at')

    # İkisini birləşdiririk
    latest_ads = list(premium_ads) + list(normal_ads)

    context = {
        'categories': categories,
        'latest_ads': latest_ads[:8]  # yalnız 8 dənə göstəririk
    }
    return render(request, 'users/home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email'] # Username-i email kimi saxlayırıq
            user.save()
            
            phone_number = form.cleaned_data.get('phone_number')
            UserProfile.objects.create(user=user, phone_number=phone_number)
            
            auth_login(request, user)
            return redirect('users:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('users:home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('users:home')

@login_required
def profile(request):
    return render(request, 'users/profile.html')


# 🔹 Balans artırma səhifəsi
@login_required
def balans_artir(request):
    if request.method == "POST":
        form = BalansArtirmaForm(request.POST, request.FILES)
        if form.is_valid():
            balans_request = form.save(commit=False)
            balans_request.user = request.user
            balans_request.status = "pending"
            balans_request.save()
            return redirect("users:profile")  # göndərdikdən sonra profile qayıdır
    else:
        form = BalansArtirmaForm()

    context = {
        "form": form,
        "card_number": "4098-5844-6360-1367"
    }
    return render(request, "users/balans_artir.html", context)
