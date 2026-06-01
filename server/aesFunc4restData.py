#aes encrypt code
# #!/usr/bin/env python3
import os
import base64
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

#load environment variables
load_dotenv()
encoded_aes_key = os.getenv("aes_key")
aes_key = base64.b64decode(encoded_aes_key)

# AES encryption function for rest data
def aes_encrypt(plaintext):
    iv = get_random_bytes(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    cipher_text_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    return iv + cipher_text_bytes

# AES decryption function for rest data
def aes_decrypt(cipher_text_bytes, input_iv):
    cipher = AES.new(aes_key, AES.MODE_CBC, input_iv)
    decrypted_text_bytes = unpad(cipher.decrypt(cipher_text_bytes), AES.block_size)
    return decrypted_text_bytes


