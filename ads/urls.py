from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('ad_create/', views.ad_create, name='ad_create'),
    path('search/', views.search_results, name='search_results'),
    path('category/<str:category_name>/', views.ad_list_by_category, name='ad_list_by_category'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    # 🔹 Premium elan URL
    path('<int:ad_id>/make_premium/', views.make_premium, name='make_premium'),
    
]
