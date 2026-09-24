"""Runnable examples of Python's commonly used built-in data types.

Run with:

	python skill_spring/concepts/builtin_data_types.py
"""

from __future__ import annotations


def show_scalar_types() -> None:
	"""Show numeric, boolean, and text values."""

	whole_number = 42
	decimal_number = 3.5
	complex_number = 2 + 3j
	is_ready = True
	greeting = "hello"

	print("\nScalars")
	print(f"int: {whole_number} + 8 = {whole_number + 8}")
	print(f"float: {decimal_number} / 2 = {decimal_number / 2}")
	print(f"complex: {complex_number} has real part {complex_number.real}")
	print(f"bool: {is_ready} behaves like the integer {int(is_ready)}")
	print(f"str: {greeting!r} becomes {greeting.upper()!r}")
	print("Difference: int, float, and complex represent increasing numeric domains; str is text.")


def show_sequence_types() -> None:
	"""Show ordered collections and their mutability."""

	names = ["Ada", "Grace"]
	coordinates = (10, 20)
	letters = "abc"
	numbers = range(1, 6)

	names.append("Katherine")

	print("\nSequences")
	print(f"list: {names} can grow with append()")
	print(f"tuple: {coordinates} is ordered but cannot be changed")
	print(f"str: {letters!r} is an immutable sequence; letters[0] is {letters[0]!r}")
	print(f"range: {list(numbers)} creates values only when needed")
	print("Difference: lists are mutable; tuples and strings are immutable; range is compact arithmetic data.")


def show_mapping_and_set_types() -> None:
	"""Show key-based lookup and unique-value collections."""

	person = {"name": "Ada", "language": "Python"}
	tags = {"python", "testing", "python"}
	fixed_tags = frozenset(tags)

	person["active"] = True
	tags.add("automation")

	print("\nMappings and sets")
	print(f"dict: person['name'] is {person['name']!r}; keys name values")
	print(f"set: {tags} removes duplicates and supports fast membership checks")
	print(f"frozenset: {fixed_tags} is immutable and can be used as a dictionary key")
	print("Difference: dict stores key/value pairs; set stores unique values; frozenset is an immutable set.")


def show_binary_types() -> None:
	"""Show immutable bytes, mutable bytearrays, and memory views."""

	raw_bytes = b"ABC"
	mutable_bytes = bytearray(raw_bytes)
	shared_view = memoryview(mutable_bytes)

	shared_view[0] = ord("Z")

	print("\nBinary data")
	print(f"bytes: {raw_bytes} is immutable binary data")
	print(f"bytearray: {mutable_bytes} changed through a memoryview")
	print(f"memoryview: {shared_view.tolist()} accesses existing bytes without copying them")
	print("Difference: bytes cannot change, bytearray can change, and memoryview shares another object's buffer.")


def show_singleton_types() -> None:
	"""Show built-in singleton markers used for special control-flow meaning."""

	missing_value = None
	unfinished_slice = Ellipsis
	unsupported_operation = NotImplemented

	print("\nSingleton markers")
	print(f"None: {missing_value!r} represents no value")
	print(f"Ellipsis: {unfinished_slice!r} is commonly used as a placeholder or in slicing APIs")
	print(f"NotImplemented: {unsupported_operation!r} tells Python an operation is not supported")
	print("Difference: these are singleton markers with semantic meaning, not normal container values.")


def main() -> None:
	"""Run all built-in data type demonstrations."""

	print("Python built-in data type examples")
	show_scalar_types()
	show_sequence_types()
	show_mapping_and_set_types()
	show_binary_types()
	show_singleton_types()


if __name__ == "__main__":
	main()
