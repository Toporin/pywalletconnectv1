from pykson import JsonObject, StringField, IntegerField, ListField

class WCEthereumTransaction(JsonObject):
    from_= StringField(serialized_name="from")
    to= StringField(null= True)
    nonce= StringField(null= True)
    gasPrice= StringField(null= True)
    gas= StringField(null= True)
    gasLimit= StringField(null= True)
    value= StringField(null= True)
    data= StringField()
    type_= IntegerField(serialized_name="type", null= True)  # EIP-2718
    maxPriorityFeePerGas = StringField(null= True) # EIP-1559
    maxFeePerGas= StringField(null= True) # EIP-1559
    accessList= ListField(str, null=True) # EIP-2930 #TODO!
    chainId= IntegerField(null= True) 
