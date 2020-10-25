def m001_initial(db):
    """
    Initial wallet table.
    """
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            ex_key TEXT NOT NULL,
            description TEXT NOT NULL,
            pub_key_no INTEGER NOT NULL
        );
    """
    )

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            ex_key TEXT NOT NULL,
            pub_key TEXT NOT NULL,
            time_to_pay INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            time TIMESTAMP NOT NULL DEFAULT (strftime('%s', 'now'))
        );
    """
    )