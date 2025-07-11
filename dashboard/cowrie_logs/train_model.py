from extract_features import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

features = extract_features('cowrie_logs/sample_log.txt')
df = pd.DataFrame(features)

X = pd.get_dummies(df[['src_ip', 'username']])
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

with open('model.pkl', 'wb') as f:
    pickle.dump(clf, f)

print(\"Model trained and saved as model.pkl\")