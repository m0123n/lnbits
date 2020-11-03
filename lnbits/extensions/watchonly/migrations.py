def m001_initial(db):
    """
    Initial wallet table.
    """
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            id TEXT NOT NULL PRIMARY KEY,
            user TEXT,
            masterpub TEXT NOT NULL,
            title TEXT NOT NULL,
            pub_key_no INTEGER NOT NULL DEFAULT 0,
            amount INTEGER NOT NULL
        );
    """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            id TEXT NOT NULL PRIMARY KEY,
            user TEXT,
            masterpub TEXT NOT NULL,
            pubkey TEXT NOT NULL,
            time_to_pay INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            time TIMESTAMP NOT NULL DEFAULT (strftime('%s', 'now'))
        );
    """
    )