# products/autocomplete.py

class TrieNode:
    def __init__(self):
        self.children = {}         # char → TrieNode
        self.ids = set()           # Product IDs passing through this node
        self.is_end_of_word = False  # Optional: marks complete names

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, product):
        """
        Insert product name into the trie and store its ID along the path.
        """
        node = self.root
        name = (product.items_name or "").strip().lower()
        if not name:
            return  # skip empty or null names

        for ch in name:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.ids.add(product.id)

        node.is_end_of_word = True  # Optional

        print(f"Inserted '{name}' for product ID {product.id}")

    def search_prefix(self, prefix):
        """
        Return product IDs that match the given prefix.
        """
        node = self.root
        prefix = (prefix or "").strip().lower()

        for ch in prefix:
            if ch not in node.children:
                print(f"No match found for prefix: '{prefix}'")
                return set()
            node = node.children[ch]

        print(f"Prefix '{prefix}' matched product IDs: {node.ids}")
        return node.ids
