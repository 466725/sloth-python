"""Order lifecycle modeled with an Enum plus a validated state machine."""

from __future__ import annotations

# Enum gives a closed set of named states: typos like "shiped" become
# AttributeError at import time instead of silently corrupting order state.
from enum import Enum, auto


class OrderStatus(Enum):
    """All possible order states. auto() assigns values so we never maintain
    numbering by hand when states are inserted or reordered."""

    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class Order:
    """An order whose status can only move through legal transitions."""

    # Class-level transition table: each state maps to the FROZENSET of states
    # it may move to. DELIVERED and CANCELLED are terminal (empty sets), which
    # is why DELIVERED -> SHIPPED is rejected. Keeping this as class data means
    # the rules are defined once, not duplicated per instance.
    VALID_TRANSITIONS: dict[OrderStatus, frozenset[OrderStatus]] = {
        OrderStatus.PENDING: frozenset({OrderStatus.CONFIRMED, OrderStatus.CANCELLED}),
        OrderStatus.CONFIRMED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset({OrderStatus.DELIVERED}),
        OrderStatus.DELIVERED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }

    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        # Status is stored as the ENUM MEMBER, never a raw string -- the type
        # system (and Enum itself) guarantees only the 5 legal values exist.
        self.status = OrderStatus.PENDING

    def transition(self, new_status: OrderStatus) -> None:
        """Move to new_status if the transition is legal, else raise ValueError."""
        # frozenset membership test: O(1) and reads as a plain rule lookup.
        allowed = self.VALID_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise ValueError(
                f"Order {self.order_id}: invalid transition "
                f"{self.status.name} -> {new_status.name}"
            )
        self.status = new_status


if __name__ == "__main__":
    order = Order("ORD-5001")

    # Legal path: PENDING -> CONFIRMED -> SHIPPED -> DELIVERED.
    for next_state in (OrderStatus.CONFIRMED, OrderStatus.SHIPPED, OrderStatus.DELIVERED):
        order.transition(next_state)
        print(f"transitioned to {order.status.name}")

    # Illegal: DELIVERED is terminal, going back to SHIPPED must fail.
    try:
        order.transition(OrderStatus.SHIPPED)
    except ValueError as exc:
        print(f"rejected: {exc}")

    # Illegal: cannot skip states (fresh order jumping straight to SHIPPED).
    fresh_order = Order("ORD-5002")
    try:
        fresh_order.transition(OrderStatus.SHIPPED)
    except ValueError as exc:
        print(f"rejected: {exc}")
