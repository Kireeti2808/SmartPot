from .parser import parse_log_line
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Used in training (reads from log file)
def extract_features(log_path):
    with open(log_path, 'r') as file:
        lines = file.readlines()

    features = []
    for line in lines:
        data = parse_log_line(line)
        if data:
            features.append({
                'src_ip': data['src_ip'],
                'username': data['username'],
                'status': 1 if data['status'] == 'succeeded' else 0
            })
    return features

# Used in Streamlit app (input is a DataFrame)
def extract_features_from_df(df):
    df = df.copy()
    df['status'] = df['status'].map({'succeeded': 1, 'failed': 0})
    
    le_ip = LabelEncoder()
    le_user = LabelEncoder()

    df['src_ip_enc'] = le_ip.fit_transform(df['src_ip'])
    df['username_enc'] = le_user.fit_transform(df['username'])

    return df[['src_ip_enc', 'username_enc']]
