import streamlit as st
import pandas as pd
import joblib
from dashboard.cowrie_logs.parser import parse_log_line
from dashboard.cowrie_logs.extract_features import extract_features_from_df
from dashboard.cowrie_logs.train_model import load_model

# Load the trained model
model = load_model('dashboard/cowrie_logs/honeypot_model.pkl')

st.set_page_config(page_title="SmartPot", layout="wide")
st.title("🛡️ SmartPot Dashboard")

uploaded_file = st.file_uploader("Upload Cowrie Log File", type=["log", "txt"])

if uploaded_file is not None:
    st.success("✅ Log file uploaded successfully!")

    # Decode and clean lines
    log_lines = uploaded_file.readlines()
    log_lines = [line.decode("utf-8") for line in log_lines]

    # Parse lines
    parsed_data = [parse_log_line(line) for line in log_lines if parse_log_line(line)]

    if parsed_data:
        df = pd.DataFrame(parsed_data)
        st.subheader("📄 Parsed Log Data")
        st.dataframe(df, use_container_width=True)

        st.subheader("🔍 Feature Extraction and Prediction")
        features = extract_features_from_df(df)
        predictions = model.predict(features)

        df['Attack Type'] = ['Malicious' if pred == 1 else 'Failed Attempt' for pred in predictions]
        st.dataframe(df[['timestamp', 'src_ip', 'username', 'Attack Type']], use_container_width=True)

        st.success("✅ Attack classification completed.")
    else:
        st.warning("⚠️ No valid log entries parsed from the uploaded file.")