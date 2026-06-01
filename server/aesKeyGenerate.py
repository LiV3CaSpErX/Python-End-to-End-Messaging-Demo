#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64, os

BLOCK_SIZE = 16  #  AES data block size 128 bits (16 bytes)
keysize = 32  # 32 bytes -> 256 bits
original_text='abcdefghijklmnopqrstuvwxyz1234567890'  # original text to be encrypted
text_in_bytes = original_text.encode()  # convert UTF 8 encoded string to bytes
print("Generating a " + str(keysize*8) +  "-bits AES key ...")

key=get_random_bytes(keysize) # generate randmom bytes array
encoded_key=base64.b64encode(key).decode('utf-8') # encode the key to base64
print("The key is generated.")
print("Encoded AES key :",end=" ")
print(encoded_key)


iv = get_random_bytes(BLOCK_SIZE) # generate a random iv
cipher = AES.new(key, AES.MODE_CBC, iv)  # new AES cipher using key generated
cipher_text_bytes = cipher.encrypt(pad(text_in_bytes, BLOCK_SIZE)) # encrypt data

# ** Decrypt message here *********

# create a new AES cipher object with the same key and mode
my_cipher = AES.new(key, AES.MODE_CBC, iv)
# Now decrypt the text using your new cipher
decrypted_text_bytes = unpad(my_cipher.decrypt(cipher_text_bytes), BLOCK_SIZE)
# Print the message in UTF8 (normal readable way)

decrypted_text = decrypted_text_bytes.decode()

if original_text == decrypted_text:
    print("aes key verification: PASSED")
else:
    print("aes key verification: FAILED")