"""Custom exception hierarchy for a banking domain, with a demo BankAccount."""

from __future__ import annotations


class BankingError(Exception):
    """Base for all banking-domain errors. Carries a stable, machine-readable code."""

    def __init__(self, message: str, error_code: str = "BANKING_ERROR") -> None:
        # super().__init__(message) keeps str(exception) behavior standard,
        # while error_code is our own structured attribute for tests/logging.
        super().__init__(message)
        self.error_code = error_code


class InsufficientFundsError(BankingError):
    """Raised when a withdrawal/transfer exceeds the available balance."""

    def __init__(self, available_balance: float, attempted_amount: float) -> None:
        self.available_balance = available_balance
        self.attempted_amount = attempted_amount
        # Message is the human story; the attributes above are the machine data
        # (tests assert on attributes, not on message text).
        super().__init__(
            f"Insufficient funds: tried to move {attempted_amount:.2f} "
            f"with only {available_balance:.2f} available",
            error_code="INSUFFICIENT_FUNDS",
        )


class InvalidAccountError(BankingError):
    """Raised when an account lookup fails or an account id is malformed."""

    def __init__(self, account_id: str) -> None:
        self.account_id = account_id
        super().__init__(
            f"Invalid account: {account_id!r}",
            error_code="INVALID_ACCOUNT",
        )


class BankAccount:
    """Minimal account supporting deposit, withdraw, and transfer."""

    def __init__(self, account_id: str, balance: float = 0.0) -> None:
        if not account_id or not account_id.strip():
            raise InvalidAccountError(account_id)
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            # Plain `raise`: this error originates from OUR validation,
            # there is no lower-level exception to chain onto.
            raise BankingError(
                f"Deposit amount must be positive, got {amount:.2f}",
                error_code="INVALID_AMOUNT",
            )
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise InsufficientFundsError(
                available_balance=self.balance, attempted_amount=amount
            )
        self.balance -= amount

    def transfer(self, target: "BankAccount", amount: float) -> None:
        try:
            self.withdraw(amount)
        except InsufficientFundsError as exc:
            # `raise ... from exc`: we TRANSLATE the withdrawal failure into a
            # transfer-level error while keeping the original as __cause__, so
            # the traceback shows the root cause explicitly.
            raise BankingError(
                f"Transfer of {amount:.2f} from {self.account_id} to "
                f"{target.account_id} failed",
                error_code="TRANSFER_FAILED",
            ) from exc
        target.deposit(amount)


if __name__ == "__main__":
    checking = BankAccount("CHK-1001", balance=150.0)
    savings = BankAccount("SAV-2001", balance=500.0)

    # Scenario 1: overdraw -> InsufficientFundsError with structured attributes.
    try:
        checking.withdraw(200.0)
    except InsufficientFundsError as exc:
        print(f"[{exc.error_code}] {exc}")
        print(f"  available={exc.available_balance:.2f} attempted={exc.attempted_amount:.2f}")
    finally:
        print(f"  checking balance after attempt: {checking.balance:.2f}\n")

    # Scenario 2: bad account id -> InvalidAccountError from the constructor.
    try:
        BankAccount("   ")
    except InvalidAccountError as exc:
        print(f"[{exc.error_code}] {exc}\n")
    finally:
        print("  invalid account was never created\n")

    # Scenario 3: failing transfer -> TRANSFER_FAILED chained from the root cause.
    try:
        checking.transfer(savings, 999.0)
    except BankingError as exc:
        print(f"[{exc.error_code}] {exc}")
        # __cause__ exists because we used `raise ... from exc`.
        print(f"  root cause: [{exc.__cause__.error_code}] {exc.__cause__}")
    finally:
        # finally runs even on failure: balances must remain consistent
        # (withdraw raised before any deposit happened).
        print(f"  checking={checking.balance:.2f} savings={savings.balance:.2f}")

    # Scenario 4: happy path stays untouched by all the error handling above.
    checking.transfer(savings, 100.0)
    print(f"\nSuccess: checking={checking.balance:.2f} savings={savings.balance:.2f}")
