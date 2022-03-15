import pyaes
import hmac
from os import urandom
from hashlib import sha256

from pykson import Pykson
from pywalletconnectv1.models.wc_encryption_payload import WCEncryptionPayload

class WCCipher:
    #def __init__(self, key: bytes):
        #self.key= key
        
    def encrypt(self, data: bytes, key: bytes= None):
        iv= urandom(16)
        aes_cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)
        aes = pyaes.Encrypter(aes_cbc, padding=pyaes.PADDING_DEFAULT)
        ciphertext = aes.feed(data) + aes.feed()
        
        payload= ciphertext+iv
        mac = hmac.new(key, payload, sha256).digest()
        
        iv_hex= iv.hex()
        ciphertext_hex= ciphertext.hex()
        mac_hex= mac.hex()
        
        #return {'data':ciphertext_hex, 'iv':iv_hex, 'hmac':mac_hex}
        return WCEncryptionPayload(data= ciphertext_hex, iv= iv_hex,  hmac= mac_hex)
        
        
    def decrypt(self, payload: WCEncryptionPayload, key: bytes= None) -> bytes :
        
        #payload = Pykson().from_json(json_text, Student)
        # ciphertext_hex= payload['data']
        # iv_hex= payload['iv']
        # mac_hex= payload['hmac']
        
        ciphertext_hex= payload.data
        iv_hex= payload.iv
        mac_hex= payload.hmac
        
        ciphertext= bytes.fromhex(ciphertext_hex)
        iv= bytes.fromhex(iv_hex)
        mac_computed= hmac.new(key, ciphertext+iv, sha256).digest()
        mac_computed_hex= mac_computed.hex()
        
        if mac_computed_hex.lower() != mac_hex.lower():
            #raise Exception(f"Wrong mac in decryption! expected {mac_hex.lower()} got {mac_computed_hex.lower()}")
            print(f"Wrong mac in decryption! expected {mac_hex.lower()} got {mac_computed_hex.lower()}")
        else:
            print(f"Correct mac: {mac_hex.lower()}")
        
        aes_cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)
        aes = pyaes.Decrypter(aes_cbc, padding=pyaes.PADDING_DEFAULT)
        decrypted = aes.feed(ciphertext) + aes.feed() 
        
        return decrypted
        
    def compute_hmac(self, data: bytes, iv: bytes, key: bytes) -> bytes:
        pass
        
    
    def randomBytes(self, size: int) -> bytes:
        return urandom(size)