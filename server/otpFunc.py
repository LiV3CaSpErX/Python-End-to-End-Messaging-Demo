import pyotp
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# load environment variables
load_dotenv()
access_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Function to generate OTP
def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    return totp, otp

# Function to verify the OTP
def verify_otp(totp, otp):
    return totp.verify(otp)

# Function to send the OTP 
def send_otp(otp):
    
    current_time = datetime.now()

    message = f"""
    Your OTP Code is: {otp}

You are trying to access SPAM2 system. Please do not share this code with anyone. If you did not request this code, please contact our support team immediately. 
Sent on {current_time}
    """

    url = f"https://api.telegram.org/bot{access_token}/sendMessage?chat_id={chat_id}&text={message}"

    # url = f"https://api.telegram.org/bot{access_token}/getUpdates"

    response = requests.get(url)




