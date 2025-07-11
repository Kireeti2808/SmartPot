import streamlit as st
import pandas as pd
import pickle
import sys
import os
sys.path.append(os.path.abspath("..")) 

from parser import parse_log_line

st.set_page_config(page_title="SmartPot Dashboard", layout="centered")
st.title("SmartPot")

# Load model
with open('../model.pkl', 'rb') as f:
    model = pickle.load(f)

st.subheader("🔐 Enter a new login attempt for prediction")

log_input = st.text_input("Log line (from Cowrie):", "")

if st.button("Predict"):
    parsed = parse_log_line(log_input)
    if not parsed:
        st.error("Invalid log format.")
    else:
        df = pd.DataFrame([{
            'src_ip': parsed['src_ip'],
            'username': parsed['username']
        }])
        X = pd.get_dummies(df)
        prediction = model.predict(X)
        result = "Attack Detected 🚨" if prediction[0] == 1 else "Safe 👍"
        st.success(f"Prediction: {result}")
