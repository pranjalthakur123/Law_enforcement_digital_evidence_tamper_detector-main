import hashlib

def hash_score(path):
    with open(path, "rb") as f:
        data = f.read()

    return 0, hashlib.sha256(data).hexdigest(), hashlib.sha3_256(data).hexdigest(), hashlib.blake2b(data).hexdigest()