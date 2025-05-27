# products/apps.py
from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MarketItems'

    def ready(self):
        from . import search_index
        from .views import load_indices
        
        # Call your index loading function
        load_indices()

