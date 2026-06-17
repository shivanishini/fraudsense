import sqlite3
conn = sqlite3.connect("fraud_transactions.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    amount REAL,

    payment_method TEXT,

    transaction_time TEXT,

    device_type TEXT,

    international TEXT,

    multiple_transactions TEXT,

    merchant_category TEXT,

    prediction TEXT,

    probability REAL
)
""")
conn.commit()
conn.close()
print("Database created successfully!")