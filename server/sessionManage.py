import sys, traceback
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP, AES  
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from sessionClass import ENC_payload

counter = 0 # counter for session ID
pub_dir = "public"
client_pub_key_base = "clientPublicKey.pem"

# Function to create session
def createSession(ip_addr):
    global counter
    counter += 1
    session_id = counter

    try:
        # Read the public key of the client
        pub_key_content=open(pub_dir+"/"+ ip_addr + "-" + client_pub_key_base,"r").read()
        pub_key=RSA.import_key(pub_key_content)
        rsa_cipher = PKCS1_OAEP.new(pub_key, hashAlgo=SHA256)

        # Generate random AES key, IV and HMAC secret
        aes_key = get_random_bytes(AES.block_size)
        aes_iv = get_random_bytes(AES.block_size)
        hmac_secret = get_random_bytes(32)

        # create the payload to be sent to the client
        # Encrypt the AES key and HMAC secret using the client's public key
        client_enc_payload = ENC_payload(
            session_id=session_id,
            enc_session_key=rsa_cipher.encrypt(aes_key),
            aes_iv=aes_iv,
            enc_hmac_secret=rsa_cipher.encrypt(hmac_secret)
        )

        # create the payload to be store in the server
        server_enc_payload = ENC_payload(
            session_id=session_id,
            enc_session_key=aes_key,
            aes_iv=aes_iv,
            enc_hmac_secret=hmac_secret
        )

    # if client public key file not found
    except:
        print("public key file not found")
        traceback.print_exc(file=sys.stdout)
        return None, None

    return client_enc_payload, server_enc_payload


