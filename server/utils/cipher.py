"""Cipher
"""

from binascii import b2a_hex, a2b_hex, Error
import Crypto.Cipher.AES as AES

class AESCipher:
    """AES Cipher
    """
    def __init__(self, key, mode, iv):
        self.key = bytes(key, encoding='utf-8')
        self.mode = mode
        self.iv = bytes(iv, encoding='utf-8')

        self.key = self.set_length(self.key, 32)
        self.iv = self.set_length(self.iv, 16)

    def set_length(self, data, length):
        datalen = len(data)
        if datalen < length:
            data = data + (b'\0' * (length - datalen))
        return data[:length]

    def make_cryptor(self):
        return AES.new(self.key, self.mode, self.iv)

    def encrypt(self, text):
        cryptor = self.make_cryptor()
        text = bytes(text, encoding='utf-8')
        length = len(text)
        if length % 16 != 0:
            text = text + (b'\0' * (16 - length % 16))
        
        return b2a_hex(cryptor.encrypt(text)).decode('utf-8')

    def decrypt(self, text):
        cryptor = self.make_cryptor()
        text = bytes(text, encoding='utf-8')
        try:
            text = a2b_hex(text)
            text = cryptor.decrypt(text)
            text.rstrip(b'\0')
            return text.decode('utf-8')
        except Error:
            return None
        return None


cipher = AESCipher('Q2UKvCVZZBj655AI7wVUuj8jE4oiaiLn', AES.MODE_CBC, 'x3qqbVLE4XAGW9RI')

def decrypt(text):
    if text is None:
        return None
    return cipher.decrypt(text)
