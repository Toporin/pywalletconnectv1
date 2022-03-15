from pykson import JsonObject, ListField, EnumStringField
from enum import Enum
 
class WCSignType(Enum):
    MESSAGE= "MESSAGE"
    PERSONAL_MESSAGE= "PERSONAL_MESSAGE"
    TYPED_MESSAGE= "TYPED_MESSAGE"
 
class WCEthereumSignMessage (JsonObject):
    raw= ListField(str)
    type_= EnumStringField(enum=WCSignType, serialized_name="type", null=False)
    
    def get(self):
        if self.type_== WCSignType.MESSAGE: 
            return self.raw[1]
        elif self.type_== WCSignType.TYPED_MESSAGE: 
            return self.raw[1]
        elif self.type_== WCSignType.PERSONAL_MESSAGE: 
            return self.raw[0]

    # /**
     # * Raw parameters will always be the message and the addess. Depending on the WCSignType,
     # * those parameters can be swapped as description below:
     # *
     # *  - MESSAGE: `[address, data ]`
     # *  - TYPED_MESSAGE: `[address, data]`
     # *  - PERSONAL_MESSAGE: `[data, address]`
     # *
     # *  reference: https://docs.walletconnect.org/json-rpc/ethereum#eth_signtypeddata
     # */
    # val data get() = when (type) {
        # WCSignType.MESSAGE -> raw[1]
        # WCSignType.TYPED_MESSAGE -> raw[1]
        # WCSignType.PERSONAL_MESSAGE -> raw[0]
