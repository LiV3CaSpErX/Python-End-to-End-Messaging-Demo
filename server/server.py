#------------------------------------------------------------------------------------------
# Server.py
#------------------------------------------------------------------------------------------
from threading import Thread    # for handling task in separate jobs we need threading
import socket           # tcp protocol
import datetime         # for composing date/time stamp
import sys              # handle system error
import traceback        # for print_exc function
import time             # for delay purpose
import pickle           # for serializing/deserializing object
from aesFunc4restData import aes_encrypt # for encrypting the data at rest
from sessionManage import createSession # for creating session
from aesFunc4SessionData import session_aes_encrypt, session_aes_decrypt # for encrypting/decrypting session data
from hmacFunc import compute_hmac # for computing the hmac
from rsaFunc import rsa_decrypt # for decrypting the data using RSA
from verifyuser import verify_user # for verifying the user credentials
from otpFunc import generate_otp, verify_otp, send_otp # for generating and verifying OTP
from rsaFunc import verify_signature # for verifying the signature
global host, port

cmd_GET_MENU = "GET_MENU"
cmd_END_DAY = "SEND_DAY_END"
cmd_PUB_KEY_EXCHANGE = "EXCHANGE"
cmd_CREATE_SESSION = "CREATE_SESSION"
cmd_END_CONNECTION = "END"
default_menu = "menu_today.txt"
default_save_base = "result-"
public_folder = "public"
data_dir = "data"
client_pub_key_file = "clientPublicKey.pem"
server_pub_key_file = "serverPublicKey.pem"
data_dir = "data"
session_id_length = 4
AES_OVERHEAD_SIZE = 16
host = socket.gethostname() # get the hostname or ip address
port = 8888                 # The port used by the server

sessions = [] # store the session information of all sessions

def find_session_by_session_id(session_id):
    for instance in sessions:
        if instance.session_id == session_id:
            return instance
    return None

def remove_session_by_session_id(session_id):
    for instance in sessions:
        if instance.session_id == session_id:
            sessions.remove(instance)
            return True
    return False

def process_connection( conn , ip_addr, MAX_BUFFER_SIZE):  
    blk_count = 0
    DATA_SIZE = 3072
    time.sleep(1)
    net_bytes = conn.recv(MAX_BUFFER_SIZE)
    dest_file = open("temp","w")  # temp file is to satisfy the syntax rule. Can ignore the file.
    while net_bytes != b'':
        if blk_count == 0: #  1st block
            usr_cmd = net_bytes[0:15].decode("utf8").rstrip()

            if cmd_PUB_KEY_EXCHANGE in usr_cmd:
                #Hints: the net_bytes after the cmd_PUB_KEY_EXCHANGE may be encrypted. 
                # The server will send the public key to the client
                # The client will send its public key to the server
                # The public key is stored in a file named "client_ip-clientPublicKey.pem"
                # The server will close the connection after the public key exchange is done.
                
                client_public_key_data = net_bytes[ len(cmd_PUB_KEY_EXCHANGE): ] # remove the PUB_KEY_EXCHANGE header
                #receive client public key
                
                # if client public key is empty, exit
                if client_public_key_data == b'':
                    print("Opps! failed to receive client public key")
                    sys.exit(0)
                
                print("Received client public key")
                try:
                    client_public_key = open(public_folder+"/"+ip_addr+"-"+client_pub_key_file,"wb")
                    client_public_key.write(client_public_key_data)
                    client_public_key.close()
                    print("Export client public key has been completed")
                except:
                    print("Opps! failed to export the client public key")
                    sys.exit(0)
                
                #send server public key
                print("Sending server public key")
                try:
                    server_pub_key = open(public_folder+"/"+server_pub_key_file,"rb")
                    server_pub_key_data = server_pub_key.read()
                    conn.sendall(server_pub_key_data)
                    server_pub_key.close()
                    print("Sending public key has been completed")
                except:
                    print("Opps! failed to send server public key")
                    sys.exit(0)
                
                return

            elif cmd_CREATE_SESSION in usr_cmd:
                #Hints: the net_bytes after the cmd_CREATE_SESSION may be encrypted. 
                # The server will create a session for the client
                # The session information will be stored in the sessions list
                # The server will send the session information to the client
                # The client will close the connection after the session information is received.
                
                # server will send banner to ask for username
                print("Received CREATE_SESSION request")
                print("Verifying user")
                conn.sendall(b"Enter Username: ")
                encrypted_username = conn.recv(MAX_BUFFER_SIZE)

                # server will send banner to ask for password
                conn.sendall(b"Enter Password: ")
                encrypted_password = conn.recv(MAX_BUFFER_SIZE)

                time.sleep(0.1) 
                # Decrypt the username and password
                username = rsa_decrypt(encrypted_username).decode('utf-8')
                password = rsa_decrypt(encrypted_password).decode('utf-8')
                # verify username and password
                if verify_user(username, password):
                    
                    print("Sending OTP for verification")
                    conn.sendall(b"User verified. Sending OTP for verification")
                    # generate OTP
                    totp, otp = generate_otp()

                    # if you want to test the OTP verification, comment out send_otp function, you can print the OTP here and verify it manually 
                    # send OTP
                    send_otp(otp)

                    # ask for OTP
                    conn.sendall(b"Enter OTP: ")
                    encrypted_user_entered_otp = conn.recv(MAX_BUFFER_SIZE)

                    user_entered_otp = rsa_decrypt(encrypted_user_entered_otp).decode('utf-8').rstrip()

                    # verify OTP
                    print("Verifying OTP")
                    if not verify_otp(totp, user_entered_otp):
                        print("Failed to verify OTP")
                        conn.sendall(b"Verification failed")
                        sys.exit(0)

                    else:

                        print("OTP verified")
                        print("User Authenticated")
                        # create session
                        client_enc_payload, server_enc_payload = createSession(ip_addr)
                        if client_enc_payload is None:
                            print("Opps! failed to create session")
                            conn.sendall(b"Verification failed")
                            sys.exit(0)
                        else:
                            sessions.append(server_enc_payload)
                            print("Session created")
                            try:

                                # send session data to client
                                enc_payload = pickle.dumps(client_enc_payload) # serialize the enc_payload object into a byte stream.
                                conn.sendall(enc_payload)
                                print("Session data sent")
                            except:
                                print("Opps! failed to send session data")
                                sys.exit(0)
                else:
                    print("Failed to verify user")
                    conn.sendall(b"Verification failed: Wrong username or password")
                    sys.exit(0)
                return
            
            elif cmd_GET_MENU in usr_cmd: # ask for menu

                # find the session 
                cur_session_id = int.from_bytes(net_bytes[ len(cmd_GET_MENU): ], byteorder='big')
                print("Received GET_MENU request")
                session = find_session_by_session_id(cur_session_id)  # find the session

                # no session found
                if session is None:
                    conn.sendall(b"Session not found")
                    print("Session not found")
                    sys.exit(0)

                # session found
                try:
                    #open the menu file
                    src_file = open(default_menu,"rb")
                except:
                    print("file not found : " + default_menu)
                    sys.exit(0)
                while True:
                    read_bytes = src_file.read(DATA_SIZE)
                    if read_bytes == b'':
                        break
                    #encrypted_data before sending
                    encrypted_bytes = session_aes_encrypt(read_bytes, session.enc_session_key, session.aes_iv)
                    #computed_hmac before sending
                    computed_hmac = compute_hmac(read_bytes, session.enc_hmac_secret)
                    #send the encrypted data and the computed hmac
                    conn.send(encrypted_bytes+computed_hmac)
                src_file.close()
                print("Processed SENDING menu") 
                return
                
            elif cmd_END_DAY in usr_cmd: # ask for to save end day order
                #find the session
                cur_session_id = int.from_bytes(net_bytes[ len(cmd_END_DAY): len(cmd_END_DAY)+ session_id_length], byteorder='big')
                print("Received Save_End_Day_Order request")
                session = find_session_by_session_id(cur_session_id)  # find the session

                # no session found
                if session is None:
                    print("Session not found")
                    conn.sendall(b"Session not found")
                    sys.exit(0)
                else:
                    conn.sendall(b"Accepting Data")

                time.sleep(1)
                hmacAndSignature = conn.recv(MAX_BUFFER_SIZE)
                
                #receive the hmac from the client
                # received_hmac_hmac = net_bytes[len(cmd_END_DAY)+session_id_length:len(cmd_END_DAY)+session_id_length+32]
                received_hmac_hmac = hmacAndSignature[:32]
                
                #receive the signature from the client
                # file_signature = net_bytes[len(cmd_END_DAY)+session_id_length+32:len(cmd_END_DAY)+session_id_length+32+256]
                file_signature = hmacAndSignature[32:]

                now = datetime.datetime.now()
                end_sale_data = ''
                filename = default_save_base +  ip_addr + "-" + now.strftime("%Y-%m-%d_%H%M") + ".bin"     
                #open the file to save the data    
                dest_file = open(filename,"wb")

                #receive the first block of END_DAY message block
                conn.sendall(b"Accepting Data")
                time.sleep(0.5)

                blk_count = blk_count + 1

        else:  # write subsequent blocks of END_DAY message block
            
            # save the end sale data
            net_bytes = conn.recv(DATA_SIZE + AES_OVERHEAD_SIZE)

            if net_bytes != b'':

                encrypted_data_bytes = net_bytes

                #decrypt the data from the client
                data_bytes = session_aes_decrypt(encrypted_data_bytes, session.enc_session_key, session.aes_iv)
                data_decoded = data_bytes.decode("utf8").rstrip()
                end_sale_data += data_decoded
            #print('Received', repr(aes_cipher_bytes))  # for debugging use

    # last block / empty block
    #compute hmac of the received data
    computed_hmac = compute_hmac(end_sale_data.encode(), session.enc_hmac_secret)
    # verify the signature of the sender
    signature_verification = verify_signature(ip_addr, end_sale_data.encode(), file_signature)

    #verify the hmac
    if received_hmac_hmac != computed_hmac:
        print("HMAC verification failed! Data integrity compromised.")
        sys.exit(0)
    
    #verify the signature
    elif not signature_verification:
        print("Signature verification failed! Cannot Verify the sender.")
        sys.exit(0)

    # save the file
    else:
        print('HMAC verification passed! Data integrity maintained.')
        print('Signature verification passed! Sender verified.')

        #encrypt the data before saving
        aes_cipher_bytes = aes_encrypt(end_sale_data.encode())
        dest_file.write(aes_cipher_bytes)
        dest_file.close()
        print("saving file as " + filename)
    
    remove_session_by_session_id(cur_session_id)
    session = None
    time.sleep(3)
    print("Processed CLOSING done") 
    return

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    process_connection( conn, ip, MAX_BUFFER_SIZE)
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " :ended")
    return

def start_server():
    global host, port
    # Here we made a socket instance and passed it two parameters. AF_INET and SOCK_STREAM. 
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    
    try:
        soc.bind((host, port))
        print('Socket bind complete')
    except socket.error as msg:
        
        print('Bind failed. Error : ' + str(sys.exc_info()))
        print( msg.with_traceback() )
        sys.exit()

    #Start listening on socket and can accept 10 connection
    soc.listen(10)
    print('Socket now listening')

    # this will make an infinite loop needed for 
    # not reseting server for every client
    try:
        while True:
            conn, addr = soc.accept()
            # assign ip and port
            ip, port = str(addr[0]), str(addr[1])
            print('Accepting connection from ' + ip + ':' + port)
            try:
                Thread(target=client_thread, args=(conn, ip, port)).start()
            except:
                print("Terrible error!")
                traceback.print_exc()
    except:
        pass
    soc.close()
    return

if __name__ == "__main__":
    start_server()  


