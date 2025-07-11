import re

def parse_log_line(line):
    pattern = r'(\\d+-\\d+-\\d+ \\d+:\\d+:\\d+)\\+\\d+ \\[.*?,(\\d+,\\d+\\.\\d+\\.\\d+\\.\\d+)\\] login attempt \\[(.+?)\\/(.+?)\\] (failed|succeeded)'
    match = re.search(pattern, line)
    if match:
        timestamp, src_ip, username, password, status = match.groups()
        return {
            \"timestamp\": timestamp,
            \"src_ip\": src_ip,
            \"username\": username,
            \"password\": password,
            \"status\": status
        }
    return None
