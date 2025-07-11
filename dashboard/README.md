# 🧠 SmartPot

This project combines a honeypot trap with machine learning to detect and analyze suspicious login attempts. Built using Cowrie (SSH honeypot), Scikit-learn, and Streamlit.

## 📁 Modules

- `parser.py` – Extracts metadata from Cowrie logs
- `extract_features.py` – Prepares login features for ML
- `train_model.py` – Trains a classifier to detect attacks
- `dashboard/app.py` – Streamlit dashboard for live predictions

## 🚀 How to Run

1. Clone the repo and navigate into it.
2. Set up a virtual environment:
    ```bash
    python3 -m venv cowrie-env
    source cowrie-env/bin/activate
    pip install -r requirements.txt
    ```
3. Train the model:
    ```bash
    python train_model.py
    ```
4. Launch dashboard:
    ```bash
    cd dashboard
    streamlit run app.py
    ```

## 🛡️ Sample Log Input Format

