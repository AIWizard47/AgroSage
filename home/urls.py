from django.urls import path
from . import views
urlpatterns = [
    path("index/",views.index,name="index"),
    path('login/', views.login_view, name='login'),
    path('logout/',views.log_out,name="logout"),
    path('register/', views.register_view, name='register'),
    path("market/",views.market,name="market"),
]
