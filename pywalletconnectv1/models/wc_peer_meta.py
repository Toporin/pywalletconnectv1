from pykson import JsonObject, StringField, ListField

class WCPeerMeta(JsonObject):
    name = StringField()
    url = StringField()
    description = StringField()
    icons = ListField(str, null= True)

    # def __init__(self, name: str="", url: str="", description: str="", icons= [""]):
        # self.name= name
        # self.url= url
        # self.description= description
        # self.icons=icons