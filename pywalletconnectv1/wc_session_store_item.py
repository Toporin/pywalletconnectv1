from pykson import JsonObject, StringField, IntegerField, ObjectField, BooleanField, DateTimeField

from .models.wc_peer_meta import WCPeerMeta
from .models.session.wc_session import WCSession

class WCSessionStoreItem(JsonObject):
    session= ObjectField(WCSession)
    chainId= IntegerField()
    peerId= StringField()
    remotePeerId= StringField()
    remotePeerMeta= ObjectField(WCPeerMeta)
    isAutoSign= BooleanField()
    date= DateTimeField()