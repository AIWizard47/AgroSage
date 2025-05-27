# in products/autocomplete.py
class TrieNode:
    def __init__(self):
        self.children = {}
        self.ids = set()   # product IDs whose name passes through here

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, product):
        node = self.root
        name = product.items_name.lower()
        for ch in name:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.ids.add(product.id)
        # you can also mark ends if needed

    def search_prefix(self, prefix):
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return set()
            node = node.children[ch]
        return node.ids
