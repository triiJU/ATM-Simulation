from __future__ import annotations

from typing import Union, Optional


class AlreadyExists(Exception):
    def __init__(self, object: any) -> None:
        self.object = object
        self.message = f"Object of type={type(object)} already exists!"
        super().__init__(self.message)


class DoesNotExist(Exception):
    def __init__(self, object: Union[any, str], *, message: str = Optional[None]):
        self.object = object
        if not message:
            self.message = f"Object of type={type(object)} does not exist!"
        else:
            self.message = message.format(object)
        super().__init__(self.message)


class BankdataUpdateFailed(Exception):
    def __init__(self, reverted: bool = False) -> None:
        self.message = "Failed to update local bankdata." + (
            "" if not reverted else " Reverted changes."
        )
        super().__init__(self.message)


class BaseTransactionException(Exception): ...


class CardLimitExceeded(BaseTransactionException):
    def __init__(self, object: int) -> None:
        self.object = object
        self.message = (
            f"The transaction-limit ({object}) of your card has been exceeded!"
        )
        super().__init__(self.message)


class WithdrawExceeded(BaseTransactionException):
    def __init__(self, object: tuple) -> None:
        self.object = object
        self.message = f"Your withdrawal-amount ({object[1]}) has exceeded your total-balance ({object[0]})!"
        super().__init__(self.message)


class CustomValidationError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)
