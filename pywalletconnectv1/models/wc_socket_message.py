from enum import Enum
from pykson import JsonObject, StringField, BooleanField, EnumStringField

class MessageType(Enum):
  SUB = 'sub'
  PUB = 'pub'

class WCSocketMessage(JsonObject):
    topic = StringField()
    type_ = EnumStringField(enum=MessageType, serialized_name="type", null=False) # type_ = StringField(serialized_name="type")
    payload = StringField()
    #silent= BooleanField(null=True) # TODO