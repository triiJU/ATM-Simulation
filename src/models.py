from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

from .exceptions import AlreadyExists, DoesNotExist, CustomValidationError


class Bank(BaseModel):
    name: str = Field(frozen=True)
    registered_cards: List["Card"] = Field(default=[])
    registered_vaults: List["Vault"] = Field(default=[])

    def register(cls, card: Card):
        if card.bank_name != cls.name:
            raise ValueError(
                f"Card 'bank_name' does not match unique identifier ({cls.name}) for specified bank."
            )
        if card in cls.registered_cards:
            raise AlreadyExists(card)
        vault = Vault(holder=card.holder, card=card)
        cls.registered_cards.append(card)
        cls.registered_vaults.append(vault)

    def deactivate(cls, card: Card) -> None:
        if card.bank_name != cls.name:
            raise ValueError(
                f"Card 'bank_name' does not match unique identifier ({cls.name}) for specified bank."
            )
        if card not in cls.registered_cards:
            raise DoesNotExist(card)
        vault = list(filter((lambda x: x.card == card), cls.registered_vaults))[0]
        cls.registered_vaults.remove(vault)
        cls.registered_cards.remove(card)


class User(BaseModel):
    first_name: str
    middle_name: Optional[str] = Field(default=None)
    last_name: str


class Card(BaseModel):
    holder: User = Field(frozen=True)
    number: str = Field(frozen=True, min_length=16, max_length=19)
    cvv: str = Field(min_length=3, max_length=4)
    bank_name: str = Field(frozen=True)
    expiration: datetime = Field(frozen=True)
    transaction_limit: int = Field(default=10000)

    @field_validator("cvv")
    def validate_cvv(cls, value: str) -> str:
        try:
            int(value)
        except ValueError:
            raise CustomValidationError("CVV can only contain valid digits from 0-9.")
        return value

    @field_validator("number")
    def validate_number(cls, value: str) -> str:
        try:
            int(value)
        except ValueError:
            raise CustomValidationError(
                "Card Number can only contain valid digits from 0-9."
            )
        return value


class Vault(BaseModel):
    holder: User = Field(frozen=True)
    card: Card = Field(frozen=True)
    balance: int = Field(default=0)
