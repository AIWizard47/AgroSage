from django.urls import path
from . import views
urlpatterns = [
    path("index/",views.index,name="index"),
    path('login/', views.login_view, name='login'),
    path('logout/',views.log_out,name="logout"),
    path('register/', views.register_view, name='register'),
    path("market/",views.market,name="market"),
    path('guidance/', views.farmer_guidance, name='farmer_guidance'),
    path('market/cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('market/list-item/', views.list_item, name='list_item'),
    path("farmer-dashboard/",views.farmer_dashboard,name="farmer_dashboard"),
    path('plants/search/', views.plant_search, name='plant_search'),
    path('payment_success/',views.payment_success,name="payment_success"),
    path('feedback/',views.feedback,name="feedback"),
    path('ai-guidance/',views.guidance,name="guidance"),
    path('search/', views.search_products, name='search_products'),
    path('about-us/',views.about_us,name='about_us'),
    path('checkout/qr/', views.payment_qr, name='payment_qr'),
    path('product-card/<int:product_id>/',views.product_card,name="product_card"),
]
