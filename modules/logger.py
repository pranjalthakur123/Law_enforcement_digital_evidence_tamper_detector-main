import datetime
import os

def log_evidence(username, filename, sha256, sha3, blake2b, result):
    os.makedirs("logs", exist_ok=True)

    log = f"""
User: {username}
File: {filename}
Time: {datetime.datetime.now()}

SHA256: {sha256}
SHA3: {sha3}
BLAKE2b: {blake2b}

Result: {result}
-------------------------
"""

    with open("logs/logs.txt", "a", encoding="utf-8") as f:
        f.write(log)