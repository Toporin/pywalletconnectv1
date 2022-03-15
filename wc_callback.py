from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from eth_hash.auto import keccak
#from pykson import Pykson

from pywalletconnectv1.wc_client import WCClient
from pywalletconnectv1.models.wc_account import WCAccount
from pywalletconnectv1.models.ethereum.wc_ethereum_sign_message import WCEthereumSignMessage, WCSignType

class WCCallback:
    
    def __init__(self, wc_client: WCClient, sato_client=None, sato_handler=None):
        self.wc_client= wc_client
        self.sato_client= sato_client # manage a pysatochip CardConnector object
        self.sato_handler= sato_handler # manage UI
        self.privkey = SigningKey.generate(curve=SECP256k1, hashfunc=sha256)
        self.pubkey = self.privkey.get_verifying_key()
        self.address= self.pubtoaddr(self.pubkey.to_string()) # to_string() actually returns bytes
        self.chain_id=1
        print(f"CALLBACK pubkey={self.pubkey.to_string().hex()}")
        print(f"CALLBACK address={self.address}")
        
    def onSessionRequest(self, id_, peer_meta):   
        print(f"CALLBACK: onSessionRequest id_={id_} - peer_meta={peer_meta}")
        
        #self.handler.wc_approve_request()
        print(f"CALLBACK Approve session request? YES!") #TODO!
        
        #val address = addressInput.editText?.text?.toString() ?: address
        #val chainId = chainInput.editText?.text?.toString()?.toIntOrNull() ?: 1
        self.wc_client.approveSession([self.address], self.chain_id)
        
    def killSession(self):
        print("CALLBACK: killSession")
    
    def onFailure(self, ex):
        print(f"CALLBACK: onFailure ex= {ex}")
        
    def onEthSign(self, id_: int, wc_ethereum_sign_message: WCEthereumSignMessage): # TODO! 
        print("CALLBACK: onEthSign")
        
        # parse msg
        raw= wc_ethereum_sign_message.raw
        wc_sign_type= wc_ethereum_sign_message.type_
        print(f"CALLBACK: onEthSign - wc_sign_type= {wc_sign_type}")
        if wc_sign_type=="MESSAGE": # also called 'standard'
            address= raw[0]
            msg_raw= raw[1]
            msg_bytes= bytes.fromhex(msg_raw.strip("0x").strip("0X"))
            print(f"CALLBACK: onEthSign - MESSAGE= {msg_bytes.decode('utf-8')}")
        elif  wc_sign_type=="PERSONAL_MESSAGE":
            address= raw[1]
            msg_raw= raw[0] # yes, it's in the other order...
            msg_bytes= bytes.fromhex(msg_raw.strip("0x").strip("0X")) #TODO
        elif wc_sign_type=="TYPED_MESSAGE":
            #TODO!
            address= raw[0]
            msg_raw= raw[1]
            msg_bytes= bytes.fromhex(msg_raw.strip("0x").strip("0X"))
        print(f"CALLBACK: onEthSign - msg_raw= {msg_raw}")
        msg_hash= self.msgtohash(msg_bytes)
        print(f"CALLBACK: onEthSign - msg_hash= {msg_hash.hex()}")
        
        # TODO: enforce low-S signature (BIP 62)
        
        do_approve= True
        if do_approve:
            print(f"CALLBACK Approve signature? YES!")
            #sign_bytes= self.privkey.sign(msg_bytes, hashfunc=sha256)
            sign_bytes= self.privkey.sign_digest(msg_hash)
            sign_hex= "0x"+sign_bytes.hex()
            self.wc_client.approveRequest(id_, sign_hex)
        else:
            print(f"CALLBACK Approve signature? NO!")
            self.wc_client.rejectRequest(id_)
        
    def onEthSignTransaction(self, id_, param):
        print("CALLBACK: onEthSignTransaction")
    
    def onCustomRequest(self, id_, param):
        print(f"CALLBACK: onCustomRequest id={id_} - param={param}")
    
    def onGetAccounts(self, id_):
        print("CALLBACK: onGetAccounts")
        account = WCAccount(
            network= self.chain_id,
            address= self.address,
        )
        self.wc_client.approveRequest(id_, account)
    
    
    ## 
    def pubtoaddr(self, pubkey:bytes)-> str:
        """
        Get address from a public key
        """
        size= len(pubkey)
        if size<64 or size>65:
            addr= f"Unexpected pubkey size {size}, should be 64 or 65 bytes"
            return addr
            #raise Exception(f"Unexpected pubkey size{size}, should be 64 or 65 bytes")
        if size== 65:
            pubkey= pubkey[1:]
        
        pubkey_hash= keccak(pubkey)
        pubkey_hash= pubkey_hash[-20:]
        addr= "0x" + pubkey_hash.hex()
        return addr
        
    def msgtohash(self, msg_bytes: bytes) -> bytes:
        
        msg_length = str(len(msg_bytes)).encode('utf-8')
        msg_encoded= b'\x19Ethereum Signed Message:\n' + msg_length + msg_bytes
        msg_hash= keccak(msg_encoded)
        return msg_hash