from dashboard.cowrie_logs.extract_features import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

# Extract features and train
features = extract_features('dashboard/cowrie_logs/sample_log.txt')
df = pd.DataFrame(features)

X = pd.get_dummies(df[['src_ip', 'username']])
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

with open('dashboard/cowrie_logs/honeypot_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("✅ Model trained and saved as honeypot_model.pkl")


# ✅ ADD THIS:
def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model
