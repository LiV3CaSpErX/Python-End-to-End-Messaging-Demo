#------------------------------------------------------------------------------------------
# Client.py
#------------------------------------------------------------------------------------------
#!/usr/bin/env python3
# Please starts the tcp server first before running this client

import datetime 
import sys              # handle system error
import socket
import os # for file operation
import time # for delay purpose
import pickle #import pickle module
from rsaFunc import rsa_decrypt, rsa_encrypt, sign_data #import rsa functions
from aesFunc4SessionData import session_aes_encrypt, session_aes_decrypt #import aes functions for session data
from hmacFunc import compute_hmac #import hmac function
global host, port, session_id, session_aes_iv, session_key, hmac_secret

host = socket.gethostname()
port = 8888         # The port used by the server
cmd_GET_MENU = b"GET_MENU"
cmd_END_DAY = b"SEND_DAY_END"
cmd_EXCHANGE_KEY = b"EXCHANGE"
cmd_CREATE_SESSION = b"CREATE_SESSION"
cmd_END_CONNECTION = b"END"
menu_file = "menu.csv"
return_file = "day_end.csv"
client_pub_key_file = "clientPublicKey.pem"
server_pub_key_file = "serverPublicKey.pem"
public_folder = "public"
data_folder = "data"
DATA_SIZE = 3072

# exchange server and client public keys
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((host, port))
    my_socket.sendall(cmd_EXCHANGE_KEY)

    #send client public key
    print("Sending client public key")
    try:
        client_pub_key = open(public_folder+"/"+client_pub_key_file,"rb")
        client_pub_key_data = client_pub_key.read()
        my_socket.sendall(client_pub_key_data)
        client_pub_key.close()
        print("sending client public key has been completed")
    except:
        print("Opps! failed to send client public key")
        sys.exit(0)
    
    time.sleep(1) # delay for 1 second

    #receive server public key
    server_pub_key_data = my_socket.recv(4096)

    # if server public key is empty, exit
    if server_pub_key_data == b'':
        print("Failed to receive server public key")
        sys.exit(0)

    print("Received server public key")
    try:
        open(public_folder+"/"+server_pub_key_file,"wb").write(server_pub_key_data)
        print("Export server public key has been completed")
    except:
        print("Opps! failed to export the server public key")
        sys.exit(0)

    my_socket.close()

# create session with server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    print("Creating session")

    my_socket.connect((host, port))
    my_socket.send(cmd_CREATE_SESSION)
    
    # server will send banner to ask for username 
    enter_username_banner = my_socket.recv(4096)
    print(enter_username_banner.decode())
    username = input()
    encrypted_username = rsa_encrypt(username.encode())
    my_socket.send(encrypted_username)

    # server will send banner to ask for password
    enter_password_banner = my_socket.recv(4096)
    print(enter_password_banner.decode())
    password = input()
    encrypted_password = rsa_encrypt(password.encode())
    my_socket.send(encrypted_password)

    server_response = my_socket.recv(4096)
    if server_response == b"Verification failed: Wrong username or password":
        print("Verification failed: Failed to Login")
        sys.exit(0)
    
    enter_otp_banner = my_socket.recv(4096)
    print(enter_otp_banner.decode())
    otp = input()
    encrypted_otp = rsa_encrypt(otp.encode())
    my_socket.send(encrypted_otp)

    # receive session data
    session_pickle_data = my_socket.recv(4096)

    if session_pickle_data == b"Verification failed":
        print("Verification failed: Failed to Login")
        sys.exit(0)
    else:   
        session_data = pickle.loads(session_pickle_data)
        session_id = session_data.session_id

        # decrypt session key and hmac secret
        session_key = rsa_decrypt(session_data.enc_session_key)
        session_aes_iv = session_data.aes_iv
        hmac_secret = rsa_decrypt(session_data.enc_hmac_secret)

        print("Session Successfully Created")
    my_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((host, port))
    my_socket.sendall(cmd_GET_MENU)
    #send session id
    my_socket.sendall(session_id.to_bytes(4, byteorder='big'))

    server_response = my_socket.recv(4096)

    if server_response == b"Session not found":
        print("Session not found")
        sys.exit(0)

    print('receiving Today Menu from server')
    #receive encrypted data
    encrypted_data = server_response[:-32]
    #receive hmac
    received_hmac = server_response[-32:]

    #decrypt data
    data = session_aes_decrypt(encrypted_data, session_key, session_aes_iv)

    #verify hmac
    computed_hmac = compute_hmac(data, hmac_secret)
    if received_hmac == computed_hmac:
        menu_file = open(menu_file,"wb")
        menu_file.write(data)
        menu_file.close()
        my_socket.close()
        print('HMAC verification passed! Data integrity maintained.')
        print('Successfully received Today Menu from server')
    else:
        print("HMAC verification failed! Data integrity compromised.")
        sys.exit(0)
#print('Received', repr(data))  # for debugging use
my_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
    my_socket.connect((host, port))
    my_socket.sendall(cmd_END_DAY)
    #send session id
    my_socket.sendall(session_id.to_bytes(4, byteorder='big'))

    server_response = my_socket.recv(4096)

    # exit if session not found
    if server_response == b"Session not found":
        print("Session not found")
        sys.exit(0)

    #open file to sign and send
    try:
        sign_file = open(return_file,"rb")
        out_file = open(return_file,"rb")
    except:
        print("file not found : " + return_file)
        sys.exit(0)
    
    whole_file = sign_file.read()

    #compute hmac 
    hmac = compute_hmac(whole_file, hmac_secret)

    #compute signature
    signature = sign_data(whole_file)
    sign_file.close()

    #send hmac
    print("Sending HMAC of sale of the day")
    my_socket.send(hmac)

    #send signature
    print("Sending signature of sale of the day")
    my_socket.send(signature)

    #wait for server response
    server_response = my_socket.recv(4096)

    #exit if session not found
    if server_response != b"Accepting Data":
        print("Session not found")
        sys.exit(0)

    #send file
    print('sending Sale of the day data to server')
    file_bytes = out_file.read(DATA_SIZE)
    while file_bytes != b'':
        # hints: need to protect the file_bytes in a way before sending out.
        # encrypt the file_bytes using session_key and session_aes_iv

        # encrypt file_bytes and send
        encrypted_bytes = session_aes_encrypt(file_bytes, session_key, session_aes_iv)
        my_socket.sendall(encrypted_bytes)
        

        file_bytes = out_file.read(DATA_SIZE) # read next block from file

    out_file.close()
    my_socket.close()
print('Successfully Sent Sale of the day to server')
# print('Sent', repr(sent_bytes))  # for debugging use
my_socket.close()

session_id = None
session_key = None
session_aes_iv = None
hmac_secret = None

print('Connection closed')