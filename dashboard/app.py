import streamlit as st
import pandas as pd
import os
import joblib
from cowrie_logs.parser import parse_log_line          
from extract_features import extract_features_from_logs

# Streamlit page setup
st.set_page_config(page_title="SmartPot Honeypot Dashboard", layout="wide")
st.title("🛡️ SmartPot: AI-Driven Honeypot Log Analyzer")

# Load the trained model
MODEL_PATH = "model.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# --- Log File Input Section ---
st.sidebar.title("Log Input Options")
log_input_option = st.sidebar.radio("Choose log source:", ("Sample Log", "Upload Your Own"))

if log_input_option == "Sample Log":
    file_path = "sample_log.txt"
    with open(file_path, "r") as f:
        log_lines = f.readlines()
else:
    uploaded_file = st.sidebar.file_uploader("Upload a Cowrie log file", type=["log", "txt"])
    if uploaded_file:
        log_lines = uploaded_file.read().decode("utf-8").splitlines()
    else:
        st.warning("Please upload a file to continue.")
        st.stop()

# --- Parse Logs ---
parsed_logs = [parse_log_line(line) for line in log_lines if parse_log_line(line)]
if not parsed_logs:
    st.error("❌ No valid log entries found.")
    st.stop()

# --- Feature Extraction ---
df_features = extract_features_from_logs(parsed_logs)
if df_features.empty:
    st.error("❌ Could not extract features from log.")
    st.stop()

# --- Model Prediction ---
predictions = model.predict(df_features)
df_results = df_features.copy()
df_results["Prediction"] = predictions
df_results["Prediction"] = df_results["Prediction"].map({0: "Benign", 1: "Malicious"})

# --- Display Results ---
st.subheader("🔍 Prediction Results")
st.dataframe(df_results, use_container_width=True)

# --- Metrics Summary ---
malicious = (df_results["Prediction"] == "Malicious").sum()
benign = (df_results["Prediction"] == "Benign").sum()

col1, col2 = st.columns(2)
col1.metric("🔴 Malicious", malicious)
col2.metric("🟢 Benign", benign)

# --- Download Option ---
csv = df_results.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Results CSV",
    data=csv,
    file_name="smartpot_predictions.csv",
    mime="text/csv"
)
