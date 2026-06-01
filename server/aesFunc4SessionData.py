from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# AES encryption function for session data
def session_aes_encrypt(plaintext, aes_key, iv):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plaintext, AES.block_size))
    return cipher_text

# AES decryption function for session data
def session_aes_decrypt(cipher_text, aes_key, iv):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
    # decrypted_text = cipher.decrypt(cipher_text)
    return decrypted_text

