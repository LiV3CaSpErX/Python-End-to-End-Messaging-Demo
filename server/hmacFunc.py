from Crypto.Hash import HMAC, SHA256

# function to compute HMAC using SHA256
def compute_hmac(data, key):
    return HMAC.new(key, data, SHA256).digest()

