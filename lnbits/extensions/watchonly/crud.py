from typing import List, Optional, Union

from lnbits.db import open_ext_db

from .models import Wallets, Payments
from lnbits.helpers import urlsafe_short_hash

from embit import bip32
from embit import ec
from embit.networks import NETWORKS
from embit import base58
from embit.util import hashlib
import io
from embit.util import secp256k1
from embit import hashes
from binascii import hexlify
from quart import jsonify
from embit import script
from embit import ec
from embit.networks import NETWORKS
from binascii import unhexlify, hexlify, a2b_base64, b2a_base64

####################Derive address#######################

def get_fresh_address(wallet_id: str):
    
    wallet = get_watch_wallet(wallet_id)
    key_num = wallet[4]
    k = bip32.HDKey.from_base58(str(wallet[2]))
    child = k.derive([0, 2])
    address = script.p2wpkh(child).address()

    update_watch_wallet(wallet_id = wallet_id, pub_key_no = key_num + 1)

    return address


####################Watch-only Wallets####################

def create_watch_wallet(*, user: str, masterpub: str, title: str) -> Wallets:
    wallet_id = urlsafe_short_hash()
    with open_ext_db("watchonly") as db:
        db.execute(
            """
            INSERT INTO wallets (
                id,
                user,
                masterpub,
                title,
                pub_key_no,
                amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (wallet_id, user, masterpub, title, 0, 0),
        )
       # weallet_id = db.cursor.lastrowid
    pubkey = get_fresh_address(wallet_id)
    print(pubkey)
    return get_watch_wallet(wallet_id)


def get_watch_wallet(wallet_id: str) -> Optional[Wallets]:
    with open_ext_db("watchonly") as db:
        row = db.fetchone("SELECT * FROM wallets WHERE id = ?", (wallet_id,))
    return Wallets.from_row(row) if row else None


def get_watch_wallets(user: str) -> List[Wallets]:
    print("poo")
    with open_ext_db("watchonly") as db:
        rows = db.fetchall("SELECT * FROM wallets WHERE user IN ?", (user,))
    return [Wallets.from_row(row) for row in rows]


def update_watch_wallet(wallet_id: str, **kwargs) -> Optional[Wallets]:
    q = ", ".join([f"{field[0]} = ?" for field in kwargs.items()])

    with open_ext_db("watchonly") as db:
        db.execute(f"UPDATE wallets SET {q} WHERE id = ?", (*kwargs.values(), wallet_id))
        row = db.fetchone("SELECT * FROM wallets WHERE id = ?", (wallet_id,))
    return Wallets.from_row(row) if row else None


def delete_watch_wallet(wallet_id: str) -> None:
    with open_ext_db("watchonly") as db:
        db.execute("DELETE FROM wallets WHERE id = ?", (wallet_id,))


###############PAYMENTS##########################

def create_payment(*, user: str, ex_key: str, description: str, amount: int) -> Payments:

    pub_key = get_fresh_address(ex_key)
    payment_id = urlsafe_short_hash()
    with open_ext_db("watchonly") as db:
        db.execute(
            """
            INSERT INTO payments (
                payment_id,
                user,
                ex_key,
                pub_key,
                amount
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (payment_id, user, ex_key, pub_key, amount),
        )
        payment_id = db.cursor.lastrowid
    return get_payment(payment_id)


def get_payment(payment_id: str) -> Payments:
    with open_ext_db("watchonly") as db:
        row = db.fetchone("SELECT * FROM payments WHERE id = ?", (payment_id,))
    return Payments.from_row(row) if row else None


def get_payments(user: str) -> List[Payments]:
    with open_ext_db("watchonly") as db:
        rows = db.fetchall("SELECT * FROM payments WHERE user IN ?", (user,))
    return [Payments.from_row(row) for row in rows]


def delete_payment(payment_id: str) -> None:
    with open_ext_db("watchonly") as db:
        db.execute("DELETE FROM payments WHERE id = ?", (payment_id,))

