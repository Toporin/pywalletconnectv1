from pykson import JsonObject, StringField, IntegerField

class WCAccount(JsonObject):
    network= IntegerField()
    address= StringField()