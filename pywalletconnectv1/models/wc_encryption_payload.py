from pykson import JsonObject, StringField

class WCEncryptionPayload(JsonObject):
    data= StringField()
    hmac= StringField()
    iv= StringField()
