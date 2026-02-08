import streamlit as st
import pandas as pd
import pickle

from dashboard.cowrie_logs.parser import parse_log_line
from dashboard.cowrie_logs.extract_features import extract_features_from_df

# ===============================
# Load trained model + columns
# ===============================
with open("dashboard/cowrie_logs/honeypot_model.pkl", "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
trained_columns = saved["columns"]

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="SmartPot", layout="wide")
st.title("🛡️ SmartPot Dashboard")

uploaded_file = st.file_uploader(
    "Upload Cowrie Log File",
    type=["log", "txt"]
)

if uploaded_file is not None:
    st.success("✅ Log file uploaded successfully!")

    # ===============================
    # Read & decode log lines
    # ===============================
    log_lines = uploaded_file.readlines()
    log_lines = [line.decode("utf-8").strip() for line in log_lines]

    # ===============================
    # Parse log lines
    # ===============================
    parsed_data = []
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            parsed_data.append(parsed)

    if not parsed_data:
        st.warning("⚠️ No valid log entries parsed from the uploaded file.")
        st.stop()

    # ===============================
    # Display parsed logs
    # ===============================
    df = pd.DataFrame(parsed_data)
    st.subheader("📄 Parsed Log Data")
    st.dataframe(df, use_container_width=True)

    # ===============================
    # Feature Extraction
    # ===============================
    st.subheader("🔍 Feature Extraction and Prediction")

    # Extract categorical features
    X = pd.get_dummies(df[['src_ip', 'username']])

    # 🔴 CRITICAL FIX: align with training columns
    X = X.reindex(columns=trained_columns, fill_value=0)

    # ===============================
    # Prediction
    # ===============================
    predictions = model.predict(X)

    # ===============================
    # Attach results
    # ===============================
    df["Attack Type"] = [
        "Malicious Login" if pred == "succeeded" else "Failed Attempt"
        for pred in predictions
    ]

    st.subheader("🚨 Attack Classification Results")
    st.dataframe(
        df[['timestamp', 'src_ip', 'username', 'Attack Type']],
        use_container_width=True
    )

    st.success("✅ Attack classification completed successfully.")
