"""Tuple practice: plain tuples, unpacking, and collections.namedtuple."""

from __future__ import annotations

# namedtuple creates a lightweight immutable record type with named fields.
from collections import namedtuple

# --- (1) Regular tuple for GPS coordinates -----------------------------------

# A tuple is ideal here: the pair is fixed-size, and position carries meaning
# (index 0 = latitude, index 1 = longitude). Immutability also makes it
# hashable, so coordinates could serve as dict keys (e.g. caching locations).
nyc_office = (40.7128, -74.0060, "floor 3", "desk 12")

# Tuple slicing works exactly like list slicing: a[start:stop] returns a new
# tuple. Here we take just the first two elements (lat, lon), dropping metadata.
coordinates_only = nyc_office[:2]
print("Full record:", nyc_office)
print("Coordinates slice:", coordinates_only)

# --- (2) Tuple unpacking in a loop -------------------------------------------

# Each row is a 3-tuple; unpacking assigns positions to names in one step,
# which is far more readable than row[0], row[1], row[2].
product_rows = [
    ("USB-C Cable", 9.99, "Accessories"),
    ("Wireless Mouse", 24.99, "Peripherals"),
    ("Mechanical Keyboard", 89.99, "Peripherals"),
]

print("\nUnpacked product rows:")
for product_name, price, category in product_rows:
    # Names from unpacking document the positions right at the loop header.
    print(f"  {product_name} | ${price:.2f} | {category}")

# --- (3) collections.namedtuple for database-like records ---------------------

# namedtuple(typename, field_names) defines a new tuple subclass whose fields
# are accessible by NAME. It stays a tuple: still immutable, still unpackable,
# still indexable -- but self-documenting.
Product = namedtuple("Product", ["id", "name", "price"])

product = Product(id="P100", name="USB-C Cable", price=9.99)

print("\nNamedtuple field access:")
print("  product.id:   ", product.id)      # attribute access beats product[0]
print("  product.name: ", product.name)    # self-documenting at the call site
print("  product.price:", product.price)

# Still a tuple underneath: indexing and unpacking keep working.
print("  product[1] (same as .name):", product[1])
product_id, product_name, product_price = product
print("  unpacked:", product_id, product_name, product_price)

# Immutability demo: product.price = 12.99 would raise AttributeError.
# namedtuple provides _replace() to derive a modified copy instead.
discounted = product._replace(price=product.price * 0.9)
print("  discounted copy:", discounted)
