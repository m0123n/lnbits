from typing import List, Optional, Union

from lnbits.db import open_ext_db

from .models import Wallets, Payments

from cryptos import *

####################Derive address#######################

def get_fresh_address(ex_key: str,):

    wallet = get_watch_wallet(wallet_id)
    key_num = wallet[4]
    print(ex_key[0:4])
    if ex_key[0:4] == "xpub":
        hd_wallet_fact = HdWalletFactory(HdWalletCoins.BITCOIN)
        hd_wallet = hd_wallet_fact.CreateFromExtendedKey("xpub_wallet", ex_key)
        hd_wallet.Generate(addr_num = key_num + 1)
        addresses = hd_wallet.GetData(HdWalletDataTypes.ADDRESSES)
        pub_key = addresses[key_num + 1].ToDict()["address"]
    elif ex_key[0:4] == "ypub" or  ex_key[0:4] == "yprv":
        hd_wallet_fact = HdWalletFactory(HdWalletCoins.BITCOIN, HdWalletSpecs.BIP49)
        hd_wallet = hd_wallet_fact.CreateFromExtendedKey("bip49_wallet", ex_key)
        hd_wallet.Generate(addr_num = key_num + 1)
        pub_key = addresses[key_num + 1].ToDict()["address"]
    elif ex_key[0:4] == "zprv":
        hd_wallet_fact = HdWalletFactory(HdWalletCoins.BITCOIN, HdWalletSpecs.BIP84)
        hd_wallet = hd_wallet_fact.CreateFromExtendedKey("bip84_wallet", ex_key)
        hd_wallet.Generate(addr_num = key_num + 1)
        pub_key = addresses[key_num + 1].ToDict()["address"]
    else:
        print("ERROR, bad key")
    update_watch_wallet(wallet_id = wallet_id, pub_key_no = key_num + 1)

    return pub_key


####################Watch-only Wallets####################

def create_watch_wallet(*, user: str, ex_key: str, description: str) -> Wallets:
    coin = Bitcoin()
    with open_ext_db("watchonly") as db:
        db.execute(
            """
            INSERT INTO wallets (
                user,
                ex_key,
                description,
                pub_key_no
            )
            VALUES (?, ?, ?, 0)
            """,
            (user, ex_key, description, amount),
        )
        weallet_id = db.cursor.lastrowid
    return get_watch_wallet(weallet_id)


def get_watch_wallet(wallet_id: str) -> Optional[Wallets]:
    with open_ext_db("watchonly") as db:
        row = db.fetchone("SELECT * FROM wallets WHERE id = ?", (wallet_id,))
    return Wallets.from_row(row) if row else None


def get_watch_wallets(user: str) -> List[Wallets]:
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

    with open_ext_db("watchonly") as db:
        db.execute(
            """
            INSERT INTO payments (
                user,
                ex_key,
                pub_key,
                amount
            )
            VALUES (?, ?, ?)
            """,
            (user, ex_key, pub_key, amount),
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

