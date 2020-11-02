from sqlite3 import Row
from typing import NamedTuple


class Wallets(NamedTuple):
    id: str
    user: str
    masterpub: str
    title: str
    amount: int
    pub_key_no: int

    @classmethod
    def from_row(cls, row: Row) -> "Wallets":
        return cls(**dict(row))

class Payments(NamedTuple):
    id: str
    user: str
    ex_key: str
    pub_key: str
    time_to_pay: str
    amount: int
    time: int

    @classmethod
    def from_row(cls, row: Row) -> "Payments":
        return cls(**dict(row))