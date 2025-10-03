from src import Machine, User, Card
from src.utils import convert_to_datetime


# create folder databases and add bankdata.pkl file inside before execution.

atm = Machine(["SBI"])
user = User(first_name="Amrit", last_name="Sutradhar")
card = Card(
    holder=user,
    number="1234123412341234",
    cvv="1234",
    bank_name="SBI",
    expiration=convert_to_datetime("1st december 2025"),
)
# print(atm.get_manager.get_bankdata)
atm.get_manager.register_account(card=card) # run this only once and comment it out later
print(atm.get_manager.get_bankdata)    # because it will throw an error as it is saved in the database already

atm.create_transaction(card=card, transaction_amount=1000, transaction_type="deposit")

print(atm.get_manager.get_bankdata)
