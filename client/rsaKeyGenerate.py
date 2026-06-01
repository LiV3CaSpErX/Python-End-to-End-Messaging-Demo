#!/usr/bin/env python3
import os, sys,traceback
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15 
from Crypto.PublicKey import RSA
from dotenv import load_dotenv

#load environment variables
load_dotenv()
secret_phrase = os.getenv("rsa_secret_passphase")
# Sample program to demonstrate the key pair export and import operations.
# main program starts here
header="A Simple Program for RSA key pair Generating"
print(header)
print("Generating an RSA key pair...")
rsakey_pair=RSA.generate(2048)  
print("Done generating the key pair.")
print("export the keypair to 'clientPrivateKey.der' with AES encryption in binary format")
prikey_in_der=rsakey_pair.export_key(format="DER", passphrase=secret_phrase, pkcs=8,protection="scryptAndAES256-CBC")
try:
    open("private/clientPrivateKey.der","wb").write(prikey_in_der)
    print("Export private key to private folder has been completed")
except:
    print("Opps! failed to export the private key")
    sys.exit(-1)

pubkey_in_pem=rsakey_pair.publickey().exportKey()
print("export the public key to 'clientPublicKey.pem' with Base64 format")
try:
    open("public/clientPublicKey.pem","wb").write(pubkey_in_pem)
    print("Export public key to public folder has been completed")
except:
    print("Opps! failed to export the public key")
    sys.exit(-1)

# now try to import back the key pair (the private key) and verify the key pair
print("now try to import back the key pair (the private key)")
prikey_bytes=open("private/clientPrivateKey.der","rb").read()
restored_keypair=RSA.import_key(prikey_bytes,passphrase=secret_phrase)
if restored_keypair == rsakey_pair:
    print("Restored the key pair successfully")
pubkey_bytes=open("public/clientPublicKey.pem","r").read()
restored_pubkey=RSA.import_key(pubkey_bytes)
if restored_pubkey == rsakey_pair.publickey():
    print("Restored the public key successfully")   