"""Unit tests for InventoryManager dict-based operations."""

from importlib import import_module

import pytest

_inventory_manager = import_module(
    "claude_code.047_cognizant_sdet_ai_builder_program.inventory_manager"
)
InventoryManager = _inventory_manager.InventoryManager


@pytest.fixture
def stocked_inventory() -> InventoryManager:
    inventory = InventoryManager()
    inventory.add_product("P100", "USB-C Cable", 9.99, 50)
    inventory.add_product("P101", "Wireless Mouse", 24.99, 5)
    inventory.add_product("P102", "Keyboard", 49.99, 10)
    return inventory


class TestAddProduct:
    def test_new_product_returns_false_and_is_stored(self):
        inventory = InventoryManager()
        assert inventory.add_product("P200", "Monitor", 149.99, 8) is False
        assert inventory.product_exists("P200") is True

    def test_duplicate_product_id_overwrites(self, stocked_inventory):
        result = stocked_inventory.add_product("P100", "Braided USB-C Cable", 12.99, 60)
        assert result is True  # signals an existing entry was replaced
        low = stocked_inventory.get_low_stock(threshold=100)
        assert low["P100"] == {"name": "Braided USB-C Cable", "price": 12.99, "quantity": 60}


class TestUpdateStock:
    def test_existing_product_updates_quantity(self, stocked_inventory):
        assert stocked_inventory.update_stock("P100", 45) is True
        assert stocked_inventory.get_low_stock(threshold=50)["P100"]["quantity"] == 45

    def test_nonexistent_product_returns_false(self, stocked_inventory):
        assert stocked_inventory.update_stock("NOPE", 10) is False


class TestGetLowStock:
    def test_threshold_10_returns_only_items_below_10(self, stocked_inventory):
        low = stocked_inventory.get_low_stock(threshold=10)
        # quantity == threshold (P102 at 10) is NOT low stock; only P101 (5) qualifies
        assert set(low.keys()) == {"P101"}
        assert low["P101"]["quantity"] == 5

    def test_threshold_10_on_empty_inventory_returns_empty_dict(self):
        assert InventoryManager().get_low_stock(threshold=10) == {}


class TestRemoveProduct:
    def test_existing_product_is_removed(self, stocked_inventory):
        assert stocked_inventory.remove_product("P101") is True
        assert stocked_inventory.product_exists("P101") is False

    def test_nonexistent_product_returns_false(self, stocked_inventory):
        assert stocked_inventory.remove_product("NOPE") is False
