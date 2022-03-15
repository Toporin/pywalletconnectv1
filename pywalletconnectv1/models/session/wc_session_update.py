from pykson import JsonObject, IntegerField, ListField, BooleanField

class WCSessionUpdate(JsonObject):
    approved= BooleanField()
    chainId= IntegerField(null= True)
    accounts= ListField(str, null=True)
