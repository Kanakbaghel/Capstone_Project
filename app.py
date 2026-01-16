import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load saved model and preprocessors
model = joblib.load('models/best_churn_model.pkl')
scaler = joblib.load('models/scaler.pkl')
le = joblib.load('models/label_encoder.pkl')
metadata = joblib.load('models/feature_metadata.pkl')

st.title("RetailSmart Churn Prediction App")
st.write("Enter customer details to predict churn risk.")

# Input fields (example – adjust based on features)
recency = st.number_input("Recency (days since last order)", min_value=0)
frequency = st.number_input("Frequency (total orders)", min_value=0)
monetary = st.number_input("Monetary (total spent)", min_value=0.0)
# Add more inputs as needed (e.g., for encoded features)

if st.button("Predict Churn"):
    # Preprocess input (scale, encode)
    input_data = pd.DataFrame([[recency, frequency, monetary, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], columns=metadata['features'][:13])  # Adjust for your features
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][1]
    st.write(f"Churn Prediction: {'Yes' if prediction == 1 else 'No'} (Probability: {prob:.2f})")
