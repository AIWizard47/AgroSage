# in products/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MarketItems
from .search_index import inverted_index
from .autocomplete import autocomplete_trie

@receiver(post_save, sender=MarketItems)
def sync_product(sender, instance, **kwargs):
    inverted_index.remove_product(instance)
    autocomplete_trie.insert(instance)
    inverted_index.add_product(instance)

@receiver(post_delete, sender=MarketItems)
def remove_product(sender, instance, **kwargs):
    inverted_index.remove_product(instance)
    # also remove from trie if you implement a remove method
