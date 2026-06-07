import re

def normalize_log(log):
    log = str(log)
    log = log.strip()
    log = log.lower()
    log = re.sub(r"\s+", " ", log)
    return log

def preprocess_logs(logs):
    cleaned = []
    for log in logs:
        normalized = normalize_log(log)
        if normalized != "":
            cleaned.append(normalized)
    return cleaned