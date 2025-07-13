## 🧠 SmartPot

SmartPot is an AI-driven SSH honeypot analysis dashboard that detects and classifies login attempts using machine learning.

Built with:
- 🐍 Python (Scikit-learn)
- 🔐 Cowrie honeypot logs
- 📊 Streamlit interface

---

## 📁 Modules

- `parser.py` – Extracts metadata from Cowrie logs
- `extract_features.py` – Transforms logs into ML features
- `train_model.py` – Trains and saves classification model
- `app.py` – Streamlit dashboard for uploading and detecting attacks

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd AI-HONEYPOT-FRAMEWORK
