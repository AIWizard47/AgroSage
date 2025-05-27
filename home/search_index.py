# products/search_index.py
import re
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        # word → set of product IDs
        self.index = defaultdict(set)

    def tokenize(self, text):
        """Lowercase + tokenize text using alphanumeric words"""
        return set(re.findall(r'\b\w+\b', text.lower()))

    def add_product(self, product):
        """
        Index product by relevant fields like name, description, category.
        """
        text_parts = [
            product.items_name or "",
            product.items_description or "",
            str(product.category.name) if hasattr(product.category, 'name') else ""
        ]
        combined_text = " ".join(text_parts)
        words = self.tokenize(combined_text)

        for word in words:
            self.index[word].add(product.id)

        print(f"Indexed Product [{product.id}]: {words}")

    def remove_product(self, product):
        """
        Remove a product's ID from all word sets in the index.
        """
        to_remove = []
        for word, id_set in self.index.items():
            id_set.discard(product.id)
            if not id_set:
                to_remove.append(word)
        
        # Clean up empty keys
        for word in to_remove:
            del self.index[word]

        print(f"Removed Product [{product.id}] from index.")

    def lookup(self, query_terms):
        """
        query_terms: list of lowercased keywords
        returns: set of product IDs matching all query terms
        """
        if not query_terms:
            return set()

        print(f"Looking up terms: {query_terms}")
        sets = [self.index.get(term, set()) for term in query_terms]
        print(f"Matched ID sets: {sets}")

        return set.intersection(*sets) if sets else set()
