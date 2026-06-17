from flask import Flask, render_template, request
import numpy as np
import joblib
import pandas as pd
import plotly.express as px
import plotly.io as pio
import sqlite3

app = Flask(__name__)

# Load model and encoders
model = joblib.load("fraud_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

@app.route('/')
def home():

    data = pd.read_csv("dataset/payment_fraud_dataset.csv")
    total_transactions = len(data)
    fraud_cases = len(data[data['Fraud'] == 1])
    safe_cases = len(data[data['Fraud'] == 0])

    fraud_count = data['Fraud'].value_counts()

    fig = px.pie(
        values=fraud_count.values,
        names=["Legitimate", "Fraud"],
        title="Fraud vs Legitimate Transactions"
    )

    graph_html = pio.to_html(fig, full_html=False)

    return render_template(
        'index.html', graph_html=graph_html,
        total_transactions=total_transactions, fraud_cases=fraud_cases, safe_cases=safe_cases
    )

@app.route('/predict', methods=['POST'])
def predict():

    try:
        amount = float(request.form['Amount'])

        payment_method = label_encoders['Payment_Method'].transform(
            [request.form['Payment_Method']]
        )[0]

        transaction_time = label_encoders['Transaction_Time'].transform(
            [request.form['Transaction_Time']]
        )[0]

        device_type = label_encoders['Device_Type'].transform(
            [request.form['Device_Type']]
        )[0]

        international = label_encoders['International'].transform(
            [request.form['International']]
        )[0]

        multiple_transactions = label_encoders['Multiple_Transactions'].transform(
            [request.form['Multiple_Transactions']]
        )[0]

        merchant_category = label_encoders['Merchant_Category'].transform(
            [request.form['Merchant_Category']]
        )[0]

        features = np.array([[
            amount,
            payment_method,
            transaction_time,
            device_type,
            international,
            multiple_transactions,
            merchant_category
        ]])

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        conn = sqlite3.connect("fraud_transactions.db")
        cursor = conn.cursor() 
        cursor.execute("""
                       INSERT INTO transactions(
                       amount,
                       payment_method,
                       transaction_time,
                       device_type,
                       international,
                       multiple_transactions,
                       merchant_category,
                       prediction,
                       probability
                       )
                       VALUES(?,?,?,?,?,?,?,?,?)
                       """,
                       (
                            amount, payment_method, transaction_time, device_type, international, multiple_transactions, merchant_category, result,
                            round(probability*100,2)
                        )
                    )
        conn.commit()
        conn.close()
        
        if prediction == 1:
            result = "⚠ Fraudulent Transaction Detected"
        else:
            result = "✅ Legitimate Transaction"

        data = pd.read_csv("dataset/payment_fraud_dataset.csv")
        total_transactions = len(data)
        fraud_cases = len(data[data['Fraud'] == 1])
        safe_cases = len(data[data['Fraud'] == 0])

        fraud_count=data['Fraud'].value_counts()

        fig = px.pie (
            values=fraud_count.values,
            names=["Legitimate","Fraud"],
            title="Fraud vs Legitimate Transactions"
        )
        
        graph_html= pio.to_html(fig, full_html=False)

        return render_template(
            'index.html',
            prediction_text=result,
            probability=round(probability * 100, 2),
            graph_html=graph_html, 
            total_transactions=total_transactions, fraud_cases=fraud_cases, safe_cases=safe_cases
        )

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)