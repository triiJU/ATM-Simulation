import pickle
from typing import List
from dataclasses import dataclass

from .models import Card, Vault, Bank
from .exceptions import AlreadyExists, DoesNotExist, BankdataUpdateFailed


@dataclass(frozen=True)
class AccessManagerConfig:
    bankdata_path: str = r"databases\bankdata.pkl"


class AccessManager:
    def __init__(self, banks_served: List["str"]) -> None:
        self.__banks_served = banks_served
        self.__bankdata_path = AccessManagerConfig().bankdata_path
        self.__bankdata_cache = self.__retrieve_bankdata()

    @property
    def get_bankdata(self) -> dict:
        return self.__bankdata_cache

    def __retrieve_bankdata(self) -> dict:
        try:
            with open(self.__bankdata_path, "rb") as reader:
                data = pickle.load(reader)
        except EOFError:
            return {bankname: Bank(name=bankname) for bankname in self.__banks_served}
        valid_banks = {}
        for bankname in self.__banks_served:
            if bankdata := data.pop(bankname, None):
                valid_banks[bankname] = bankdata
            else:
                valid_banks[bankname] = Bank(name=bankname)
        return valid_banks

    def push_bankdata_updates(self) -> None:
        with open(self.__bankdata_path, "rb+") as handler:
            try:
                data = pickle.load(handler)
            except EOFError:
                data = {}
            data.update(self.__bankdata_cache)
            handler.seek(0)
            pickle.dump(data, handler)
            handler.truncate()

    def restore_bankdata_cache(self) -> None:
        self.__bankdata_cache = self.__retrieve_bankdata()

    def retrieve_card(self, number: str, cvv: str) -> Card:
        self.restore_bankdata_cache()
        for bank in self.__bankdata_cache.values():
            for card in bank.registered_cards:
                if (number == card.number) and (cvv == card.cvv):
                    return card

    def retrieve_vault(self, card: Card) -> Vault:
        self.restore_bankdata_cache()
        bank = self.__bankdata_cache.get(card.bank_name, None)
        if not bank:
            raise DoesNotExist(
                card.bank_name, message="Bank with name:{0} does not exist!"
            )
        for vault in bank.registered_vaults:
            if card == vault.card:
                return vault

    def register_account(self, card: Card) -> None:
        if self.retrieve_card(card.number, card.cvv):
            raise AlreadyExists(card)
        bank = self.__bankdata_cache.get(card.bank_name, None)
        if not bank:
            raise DoesNotExist(
                card.bank_name, message="Bank with name:{0} does not exist!"
            )
        bank.register(card)
        try:
            self.push_bankdata_updates()
        except Exception:
            bank.deactivate(card)
            raise BankdataUpdateFailed(reverted=True)

    def deactivate_account(self, card: Card) -> None:
        if not self.retrieve_card(card.number, card.cvv):
            raise DoesNotExist(card)
        bank = self.__bankdata_cache.get(card.bank_name, None)
        if not bank:
            raise DoesNotExist(
                card.bank_name, message="Bank with name:{0} does not exist!"
            )
        bank.deactivate(card)
        try:
            self.push_bankdata_updates()
        except Exception:
            bank.register(card)
            raise BankdataUpdateFailed(reverted=True)
