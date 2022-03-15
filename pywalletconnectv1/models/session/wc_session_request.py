from pykson import JsonObject, StringField, IntegerField, ObjectField

from ..wc_peer_meta import WCPeerMeta

class WCSessionRequest(JsonObject):
    peerId= StringField()
    peerMeta= ObjectField(WCPeerMeta)
    chainId= IntegerField(null= True)