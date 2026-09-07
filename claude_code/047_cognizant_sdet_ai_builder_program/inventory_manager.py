"""InventoryManager: dictionary-based inventory tracking practice.

Internal store shape:
    {product_id: {"name": str, "price": float, "quantity": int}}
"""

from __future__ import annotations

from typing import Any


class InventoryManager:
    """Manages products keyed by product_id using a dict internally."""

    def __init__(self) -> None:
        self._products: dict[str, dict[str, Any]] = {}

    def add_product(self, product_id: str, name: str, price: float, quantity: int) -> bool:
        """Add a product, overwriting any existing entry with the same product_id.

        Returns True if an existing product was overwritten, False if it is new.
        """
        # `in` tests dict keys directly (O(1)); plain assignment on an existing
        # key overwrites the value -- that is standard dict semantics.
        existed = product_id in self._products
        self._products[product_id] = {"name": name, "price": price, "quantity": quantity}
        return existed

    def update_stock(self, product_id: str, quantity: int) -> bool:
        """Set the quantity of an existing product. Returns False if not found."""
        # dict.get() returns the value or None instead of raising KeyError,
        # so a missing ID becomes a clean boolean result.
        product = self._products.get(product_id)
        if product is None:
            return False
        # get() returns a live reference to the stored (mutable) dict,
        # so mutating it here updates the store in place.
        product["quantity"] = quantity
        return True

    def product_exists(self, product_id: str) -> bool:
        """Return True if the product_id is in the inventory."""
        # The `in` operator is the idiomatic, fastest existence check for dict keys.
        return product_id in self._products

    def remove_product(self, product_id: str) -> bool:
        """Remove a product. Returns True if it existed, False otherwise."""
        # dict.pop(key, None) removes AND returns the value in one call;
        # the None default avoids KeyError and doubles as the existence signal.
        return self._products.pop(product_id, None) is not None

    def get_low_stock(self, threshold: int) -> dict[str, dict[str, Any]]:
        """Return products whose quantity is below the threshold."""
        # dict.items() yields (key, value) pairs so the filter keeps the
        # product_id attached to each matching product dict.
        return {
            product_id: product
            for product_id, product in self._products.items()
            if product["quantity"] < threshold
        }


if __name__ == "__main__":
    inventory = InventoryManager()
    inventory.add_product("P100", "USB-C Cable", 9.99, 50)
    inventory.add_product("P101", "Wireless Mouse", 24.99, 3)
    inventory.add_product("P102", "Keyboard", 49.99, 0)

    inventory.update_stock("P100", 45)
    inventory.remove_product("P102")

    print("P101 exists:", inventory.product_exists("P101"))
    print("P102 exists:", inventory.product_exists("P102"))
    print("Low stock (< 5):", inventory.get_low_stock(5))
