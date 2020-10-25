from typing import NamedTuple


class Wallets(NamedTuple):
    id: str
    user: str
    ex_key: str
    description: str
    amount: int
    pub_key_no: int

class Payments(NamedTuple):
    id: str
    user: str
    ex_key: str
    pub_key: str
    time_to_pay: str
    amount: int
    time: int