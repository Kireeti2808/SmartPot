import json

def parse_log_line(line):
    try:
        log = json.loads(line)
        if log.get("eventid") in ["cowrie.login.failed", "cowrie.login.success"]:
            return {
                "timestamp": log.get("timestamp", "")[:19].replace("T", " "),
                "src_ip": log.get("src_ip", "0.0.0.0"),
                "username": log.get("username", "unknown"),
                "password": log.get("password", "unknown"),
                "status": "succeeded" if log["eventid"] == "cowrie.login.success" else "failed"
            }
    except json.JSONDecodeError:
        return None
