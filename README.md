# Python-End-to-End-Messaging-Demo

End to End Messaging Program

Please Disable the Telegram Bot to sending OTP and print out the OTP if you wanna test it locally.

---

## User Creation and Registration

Note: you should have set necessary DB_information (like DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE) inside environment variables (.env file)

1. Open terminal
2. CD to the server/db directory  
   2.1 db directory should contain createSchema.py and createUser.py
   
   2.2 For First time starting Program, you need to run createSchema.py to create database Schema.
   
4. Type "python createUser.py"  
   3.1 You should see:-

    Welcome to User Registration System
    Enter your username:
    Enter your password:

    Enter the username and password you wanna Register to the System

    3.2. If the user is registered successfully. You should see:-

    User registered successfully

---

## AES key Generating (for server)

1. Open terminal
2. CD to the server directory
3. Type "python aesKeyGenerate.py"  
   3.1 You should see:-

    Generating a 256-bits AES key ...
    The key is generated.
    Encoded AES key: some random key with encoded format (eg. rUpAR4yUVqh5Kvyyvlgp8yJ93D3kYrsGsZtSZCXMCWI=)
    aes key verification: PASSED

4. You can copy the key and paste in the environment variables (.env file) for encrypting and decrypting data at rest

---

## RSA key Generating (for both server and client)

Note: you should have set some rsa secret passphase to encrypt the rsa private key inside environment variables (.env file)

1. Open terminal
2. CD to the server or client directory
3. Type "python rsaKeyGenerate.py"  
   3.1 for server side, You should see:-

    A Simple Program for RSA key pair Generating
    Generating an RSA key pair...
    Done generating the key pair.
    export the keypair to 'serverPrivateKey.der' with AES encryption in binary format
    Export private key to private folder has been completed
    export the public key to 'serverPublicKey.pem' with Base64 format
    Export public key to public folder has been completed
    now try to import back the key pair (the private key)
    Restored the key pair successfully
    Restored the public key successfully

    3.2 for client side, You should see:-

    A Simple Program for RSA key pair Generating
    Generating an RSA key pair...
    Done generating the key pair.
    export the keypair to 'clientPrivateKey.der' with AES encryption in binary format
    Export private key to private folder has been completed
    export the public key to 'clientPublicKey.pem' with Base64 format
    Export public key to public folder has been completed
    now try to import back the key pair (the private key)
    Restored the key pair successfully
    Restored the public key successfully

---

## Using the Program (client and server)

1. Run 2 separate terminal

Server Setup Part:

2. CD to the server directory (using terminal 1)  
   2.1 Server directory should contain server.py and menu_today.txt files
   
3. Type "python server.py"  
   3.1 In server You should see:-  
      a. Socket Created  
      b. Socket bind complete  
      c. Socket now listening  
      Your server program is successfully setup and is listening for connection now

Client Part:  

4. CD to the client directory (using terminal 2)  
   4.1 Client directory should contain client.py and day_end.csv files

5. Type "python client.py"  
   5.1 In client You should see:-  

    Sending client public key
    sending client public key has been completed
    Received server public key
    Export server public key has been completed
    Creating session  

    5.2 In client You should also see:-  

    Enter Username:

    5.3 Type in the username

    5.4 After that You should see:-

    Enter Password:

    5.5 Type in the password

    5.6 OTP will Send via Telegram and You should see:-

    Enter OTP:

    5.7 Type in the OTP

    5.8 After Successful login. Client will receive Today Menu from Server. You should see:-

    Session Successfully Created
    receiving Today Menu from server
    HMAC verification passed! Data integrity maintained.
    Successfully received Today Menu from server

    5.9 After that Client will send Closing Day information to Sever. You should see:-

    Sending HMAC of sale of the day
    Sending signature of sale of the day
    sending Sale of the day data to server
    Successfully Sent Sale of the day to server

    5.10 If everything is done Connection terminated and back to command prompt. You should see:-

    Connection closed  

6. You should see menu.csv file in the client directory

Server Part :  

7. Server will accept connection from the clients    
   7.1 If the Client Connect to Server. You should see:-  

   Accepting connection from (client_ip:port)
   Received client public key
   Export client public key has been completed
   Sending server public key
   Sending public key has been completed
   Connection (client_ip:port) :ended

   7.2 If the Client Try to create a Session. You should see:-  
   
   Accepting connection from (client_ip:port)
   Received CREATE_SESSION request
   Verifying user
   
   7.3 If the Client enter the Correct credential (username, password),
   Server will generate OTP and sent via Telegram. You should see:-
   
   Sending OTP for verification
   
   7.4 If the Client Enter the Correct OTP. Server will create the Session You should see:-
   
   Verifying OTP
   OTP verified
   User Authenticated
   Session created
   Session data sent
   Connection (client_ip:port) :ended

   7.5. If the Client Request to get menu from server, Server will send the menu to client. You should see:-
   
   Accepting connection from (client_ip:port)
   Received GET_MENU request
   Processed SENDING menu
   Connection (client_ip:port) :ended
   
   7.6. If the Client Request to save day-closing information to server,
   Server will accept day-closing information from client. You should see:-
   
   Accepting connection from (client_ip:port)
   Received Save_End_Day_Order request
   HMAC verification passed! Data integrity maintained.
   Signature verification passed! Sender verified.
   saving file as "result-<IP Address>.bin"
   Processed CLOSING done
   Connection (client_ip:port) :ended

8. File "result-<IP Address>.bin" received by server

---

## Reading Encrypted Data at rest

1. Open terminal
2. CD to the server directory
3. Type "python readDayEndSale.py <file-you-want-to-decrypt>.bin" (eg. result-<IP Address>.bin)

    3.1. You should also see:-

    Enter username:

    3.2 Type in the username, After that You should also see:-

    Enter password:

    3.3 Type in the password, if the credential are correct, You should also see:-

    Decrypting the file content with the AES key
    data chunk size; <file-size>
    Total of <file-size> bytes written to result-<IP Address>.csv

4. File result-<IP Address>.bin is successfully decrypt into result-<IP Address>.csv.
   Now you should see result-<IP Address>.csv
