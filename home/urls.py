from django.urls import path
from . import views
urlpatterns = [
    path("index/",views.index,name="index"),
    path('login/', views.login_view, name='login'),
    path('logout/',views.log_out,name="logout"),
    path('register/', views.register_view, name='register'),
    path("market/",views.market,name="market"),
    path('ai-guidance/', views.farmer_guidance, name='farmer_guidance'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('market/list-item/', views.list_item, name='list_item'),
    path("farmer-dashboard/",views.farmer_dashboard,name="farmer_dashboard"),
    path('plants/search/', views.plant_search, name='plant_search'),
    path('payment_success/',views.payment_success,name="payment_success"),
    path('feedback/',views.feedback,name="feedback"),
    path('guidance/',views.guidance,name="guidance"),
    path('search/', views.search_products, name='search_products'),
]
