from pykson import JsonObject, StringField, IntegerField, ListField, BooleanField, ObjectField

from ..wc_peer_meta import WCPeerMeta

class WCApproveSessionResponse(JsonObject):
    approved= BooleanField() # default True TODO
    chainId= IntegerField()
    accounts= ListField(str)
    peerId= StringField(null= True)
    peerMeta= ObjectField(WCPeerMeta, null=True)