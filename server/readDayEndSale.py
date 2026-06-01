from aesFunc4restData import aes_decrypt
import sys, traceback, os
from verifyuser import verify_user

# Get the first file in the directory if no file is provided
bin_files = [f for f in os.listdir() if f.endswith('.bin')]
try:
    fn = bin_files[0]
except:
    print("No file found")
    sys.exit(0)

# Get the file name from the command line argument
if len(sys.argv) == 2:
    fn=sys.argv[1]

# Get the username and password from the user
username = input("Enter username: ")
password = input("Enter password: ")

# Verify the user
if verify_user(username,password):
    
    try:
        print("Decrypting the file content with the AES key")
        file=open(fn,"rb").read()
        iv=file[:16]
        data=file[16:]
        print(f"data chunk size; {len(data)}")

        # Decrypt the file content
        plain_text = aes_decrypt(data,iv)

        # now save the encrypted file
        csv_file = fn.replace(".bin",".csv")
        out_bytes=open(csv_file,"wb").write(plain_text)
        print(f"Total of {out_bytes} bytes written to {csv_file}")
    except:
        print("Opps")
        traceback.print_exc(file=sys.stdout)

else:
    print("Invalid user")
    sys.exit(0)
