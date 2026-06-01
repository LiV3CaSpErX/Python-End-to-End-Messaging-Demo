class ENC_payload:
    # A data class to store a session data.
    # The session content has been encrypted using an session key (AES key).
    # The session key and hmac secret are encrypted by a client public key and stored in the enc_session_key, enc_hmac_secret instance attribute. 
    def __init__(self, session_id, enc_session_key, aes_iv, enc_hmac_secret):
        # Increment the counter and assign the new ID
        self.session_id = session_id
        self.enc_session_key = enc_session_key
        self.aes_iv = aes_iv
        self.enc_hmac_secret = enc_hmac_secret
