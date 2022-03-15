from pykson import JsonObject, StringField

class WCEthereumTransaction(JsonObject):
    from_= StringField(serialized_name="from")
    to= StringField(null= True)
    nonce= StringField(null= True)
    gasPrice= StringField(null= True)
    gas= StringField(null= True)
    gasLimit= StringField(null= True)
    value= StringField(null= True)
    data= StringField()