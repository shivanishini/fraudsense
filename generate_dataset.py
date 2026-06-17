import pandas as pd
import random

data = []

payment_methods = ["UPI", "Card", "NetBanking"]
transaction_times = ["Day", "Evening", "Night"]
device_types = ["Mobile", "Laptop", "Tablet"]
international_options = ["Yes", "No"]
multiple_transactions_options = ["Yes", "No"]
merchant_categories = [
    "Electronics",
    "Food",
    "Grocery",
    "Luxury",
    "Travel",
    "Jewelry"
]

for i in range(1000):

    amount = random.randint(100, 500000)

    payment_method = random.choice(payment_methods)
    transaction_time = random.choice(transaction_times)
    device_type = random.choice(device_types)
    international = random.choice(international_options)
    multiple_transactions = random.choice(multiple_transactions_options)
    merchant_category = random.choice(merchant_categories)

    # Fraud logic
    fraud_score = 0

    if amount > 30000:
        fraud_score += 3

    if international == "Yes":
        fraud_score += 3

    if multiple_transactions == "Yes":
        fraud_score += 2

    if merchant_category in ["Luxury", "Jewelry"]:
        fraud_score += 2

    if transaction_time == "Night":
        fraud_score += 1

    # add some randomness to the fraud score
    fraud_score = random.choice([0,0,1])

    fraud = 1 if fraud_score >= 5 else 0
        
    data.append([
        amount,
        payment_method,
        transaction_time,
        device_type,
        international,
        multiple_transactions,
        merchant_category,
        fraud
    ])

columns = [
    "Amount",
    "Payment_Method",
    "Transaction_Time",
    "Device_Type",
    "International",
    "Multiple_Transactions",
    "Merchant_Category",
    "Fraud"
]

df = pd.DataFrame(data, columns=columns)
print("Rows generated:", len(data))

df.to_csv("dataset/payment_fraud_dataset.csv", index=False)

print("Dataset generated successfully!")