import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load saved model and tools (paths for your repo: Exported_files/Phase 2/Models/)
model = joblib.load('Exported_files/Phase 2/Models/best_churn_model.pkl')
scaler = joblib.load('Exported_files/Phase 2/Models/scaler.pkl')
metadata = joblib.load('Exported_files/Phase 2/Models/feature_metadata.pkl')

st.title("RetailSmart Churn Prediction – MLOps App 🚀")
st.write("Enter customer details to predict churn risk.")

# Input fields (match your 23 features – add more sliders if needed)
recency = st.number_input("Recency (days since last order)", min_value=0, value=100)
frequency = st.number_input("Frequency (total orders)", min_value=0, value=1)
monetary = st.number_input("Monetary (total spent)", min_value=0.0, value=100.0)
avg_order_value = st.number_input("Avg Order Value", min_value=0.0, value=50.0)
response_rate = st.number_input("Response Rate", min_value=0.0, max_value=1.0, value=0.1)
tenure = st.number_input("Tenure (days)", min_value=0, value=365)
# Placeholders for other features (set to 0 – adjust if you have more inputs)
other_features = [0] * (len(metadata['features']) - 6)  # 6 inputs above, rest 0

if st.button("Predict Churn"):
    # Build input
    input_values = [recency, frequency, monetary, avg_order_value, response_rate, tenure] + other_features
    input_data = pd.DataFrame([input_values], columns=metadata['features'])
    
    # Scale and predict
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][1]
    
    st.write(f"Churn Prediction: {'High Risk' if prediction == 1 else 'Low Risk'}")
    st.write(f"Probability: {prob:.2f}")
    if prob > 0.5:
        st.write("💡 Action: Send re-engagement campaign!")
