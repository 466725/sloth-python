"""Payment processor hierarchy: abstract base class + polymorphic gateway."""

from __future__ import annotations

# ABC + abstractmethod turn PaymentProcessor into a CONTRACT: any subclass that
# forgets a required method fails at INSTANTIATION time (TypeError), not later
# at a mysterious call site -- exactly the fast feedback an SDET wants.
from abc import ABC, abstractmethod
from uuid import uuid4


class PaymentProcessor(ABC):
    """Contract every payment processor must fulfill."""

    @abstractmethod
    def process_payment(self, amount: float) -> str:
        """Charge amount and return a confirmation message."""

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Return True when the processor's credentials/configuration are usable."""

    @abstractmethod
    def get_transaction_id(self) -> str:
        """Return a unique id for the current transaction."""


class CreditCardProcessor(PaymentProcessor):
    """Concrete processor: charges via a card network."""

    def __init__(self, card_number: str, cardholder: str) -> None:
        self._card_number = card_number  # kept private; never logged in full
        self.cardholder = cardholder

    def validate_credentials(self) -> bool:
        # Toy check for the exercise: 16 digits. Real systems call the network.
        return self._card_number.isdigit() and len(self._card_number) == 16

    def get_transaction_id(self) -> str:
        return f"CC-{uuid4().hex[:8]}"

    def process_payment(self, amount: float) -> str:
        if not self.validate_credentials():
            raise ValueError("Invalid credit card credentials")
        transaction_id = self.get_transaction_id()
        masked = "*" * 12 + self._card_number[-4:]
        return f"[{transaction_id}] Charged {amount:.2f} to card {masked} ({self.cardholder})"


class UPIProcessor(PaymentProcessor):
    """Concrete processor: charges via UPI handle."""

    def __init__(self, upi_id: str) -> None:
        self.upi_id = upi_id

    def validate_credentials(self) -> bool:
        # UPI handles look like name@bank; string-method check only.
        return self.upi_id.count("@") == 1 and all(self.upi_id.split("@"))

    def get_transaction_id(self) -> str:
        return f"UPI-{uuid4().hex[:8]}"

    def process_payment(self, amount: float) -> str:
        if not self.validate_credentials():
            raise ValueError("Invalid UPI id")
        transaction_id = self.get_transaction_id()
        return f"[{transaction_id}] Charged {amount:.2f} via UPI {self.upi_id}"


class PaymentGateway:
    """Depends ONLY on the PaymentProcessor abstraction (dependency injection).

    The gateway never imports or name-checks concrete classes: duck-typing
    against the ABC contract is what makes this polymorphic. Adding a new
    processor (PayPal, wallet, ...) requires zero changes here.
    """

    def __init__(self, processor: PaymentProcessor) -> None:
        self._processor = processor

    def checkout(self, amount: float) -> str:
        # isinstance check against the ABC documents the contract and fails
        # fast with a clear error instead of an AttributeError deep inside.
        if not isinstance(self._processor, PaymentProcessor):
            raise TypeError("processor must implement the PaymentProcessor contract")
        return self._processor.process_payment(amount)


if __name__ == "__main__":
    # Polymorphism: one gateway code path, two different processor behaviors.
    processors: list[PaymentProcessor] = [
        CreditCardProcessor(card_number="4111111111111111", cardholder="John Doe"),
        UPIProcessor(upi_id="john@okaxis"),
    ]

    for processor in processors:
        gateway = PaymentGateway(processor)
        print(gateway.checkout(499.99))

    # Contract enforcement demo: an ABC missing an implementation cannot be built.
    class IncompleteProcessor(PaymentProcessor):
        pass

    try:
        IncompleteProcessor()
    except TypeError as exc:
        print(f"\ncontract enforced: {exc}")
