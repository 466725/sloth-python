"""Unit tests for tuple_examples: slicing, unpacking, namedtuple behavior."""

from importlib import import_module

import pytest

_tuple_examples = import_module(
    "claude_code.047_cognizant_sdet_ai_builder_program.tuple_examples"
)


class TestGpsSlicing:
    def test_first_two_elements_are_coordinates(self):
        nyc_office = (40.7128, -74.0060, "floor 3", "desk 12")
        assert nyc_office[:2] == (40.7128, -74.0060)

    def test_slice_returns_new_tuple_without_mutating_original(self):
        nyc_office = (40.7128, -74.0060, "floor 3", "desk 12")
        nyc_office[:2]
        assert nyc_office == (40.7128, -74.0060, "floor 3", "desk 12")

    def test_module_coordinates_match_expected_slice(self):
        assert _tuple_examples.coordinates_only == (40.7128, -74.0060)


class TestTupleUnpacking:
    def test_unpacking_assigns_positions_in_order(self):
        row = ("USB-C Cable", 9.99, "Accessories")
        product_name, price, category = row
        assert product_name == "USB-C Cable"
        assert price == 9.99
        assert category == "Accessories"

    def test_loop_unpacking_covers_all_module_rows(self):
        collected = []
        for product_name, price, category in _tuple_examples.product_rows:
            collected.append((product_name, price, category))
        assert collected == [
            ("USB-C Cable", 9.99, "Accessories"),
            ("Wireless Mouse", 24.99, "Peripherals"),
            ("Mechanical Keyboard", 89.99, "Peripherals"),
        ]


class TestProductNamedTuple:
    def test_field_access_by_name(self):
        product = _tuple_examples.product
        assert product.id == "P100"
        assert product.name == "USB-C Cable"
        assert product.price == 9.99

    def test_named_field_matches_positional_index(self):
        product = _tuple_examples.product
        assert product[1] == product.name

    def test_namedtuple_still_unpacks_like_a_tuple(self):
        product_id, product_name, product_price = _tuple_examples.product
        assert (product_id, product_name, product_price) == ("P100", "USB-C Cable", 9.99)


class TestImmutability:
    def test_assigning_tuple_item_raises_type_error(self):
        coordinates = (40.7128, -74.0060)
        with pytest.raises(TypeError):
            coordinates[0] = 51.5074

    def test_assigning_namedtuple_field_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            _tuple_examples.product.price = 12.99
