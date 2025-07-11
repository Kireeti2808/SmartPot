from parser import parse_log_line

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
