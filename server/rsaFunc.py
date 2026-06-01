import os, sys,traceback
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from dotenv import load_dotenv

private_dir = "private"
public_dir = "public"
server_priv_key = "serverPrivateKey.der"
client_pub_key_base = "clientPublicKey.pem"

#load environment variables
load_dotenv()
secret_phrase = os.getenv("rsa_secret_passphase")

# Function to decrypt the data using RSA
def rsa_decrypt(ct):
    try:
        priv_key_content=open(private_dir+"/"+server_priv_key,"rb").read()
        pri_key=RSA.import_key(priv_key_content,passphrase=secret_phrase)
        cipher = PKCS1_OAEP.new(pri_key , hashAlgo=SHA256)
        plain_text = cipher.decrypt(ct)
        return plain_text
    except:
        print("Opps! failed to import the private key")
        traceback.print_exc(file=sys.stdout)
        return None

# Function to verify the signature of the data
def verify_signature(ip_addr,data,signature):
    try:
        pub_key_content=open(public_dir+"/"+ ip_addr + "-" + client_pub_key_base,"r").read()
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