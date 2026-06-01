import os, sys,traceback
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from dotenv import load_dotenv

private_dir = "private"
public_dir = "public"
client_priv_key = "clientPrivateKey.der"
server_public_key = "serverPublicKey.pem"
client_public_key = "clientPublicKey.pem"
#load environment variables
load_dotenv()
secret_phrase = os.getenv("rsa_secret_passphase")

# Function to decrypt the data using RSA
def rsa_decrypt(ct):
    try:
        priv_key_content=open(private_dir+"/"+client_priv_key,"rb").read()
        pri_key=RSA.import_key(priv_key_content,passphrase=secret_phrase)
        cipher = PKCS1_OAEP.new(pri_key , hashAlgo=SHA256)
        plain_text = cipher.decrypt(ct)
        return plain_text
    except:
        print("Opps! failed to import the private key")
        traceback.print_exc(file=sys.stdout)
        return None

# Function to encrypt the data using RSA
def rsa_encrypt(data):
    try:
        pub_key_content=open(public_dir+"/"+server_public_key,"r").read()
        pub_key=RSA.import_key(pub_key_content)
        rsa_cipher = PKCS1_OAEP.new(pub_key, hashAlgo=SHA256)
        encrypted = rsa_cipher.encrypt(data)
        return encrypted
    except:
        print("Opps! failed to import the public key")
        traceback.print_exc(file=sys.stdout)
        return None

# Function to sign the data
def sign_data(data):
    try:
        priv_key_content=open(private_dir+"/"+client_priv_key,"rb").read()
        pri_key=RSA.import_key(priv_key_content,passphrase=secret_phrase)
        hashed_message = SHA256.new(data)
        signer = pkcs1_15.new(pri_key)
        signature = signer.sign(hashed_message)
        return signature
    except:
        print("Opps! failed to sign the data")
        traceback.print_exc(file=sys.stdout)
        return None

# Function to verify the signature of the data
def verify_signature(data,signature):
    try:
        pub_key_content=open(public_dir+"/"+client_public_key,"r").read()
        pub_key=RSA.import_key(pub_key_content)
        hashed_message = SHA256.new(data)
        verifier = pkcs1_15.new(pub_key)
        try:
            verifier.verify(hashed_message,signature)
            return True
        except:
            print("Opps! failed to verify the signature")
            traceback.print_exc(file=sys.stdout)
            return False
    except:
        print("Opps! failed to verify the signature")
        traceback.print_exc(file=sys.stdout)
        return False
    
