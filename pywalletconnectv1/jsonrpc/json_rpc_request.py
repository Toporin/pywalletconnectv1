from pykson import JsonObject, StringField, IntegerField, ListField, ObjectListField, MultipleChoiceStringField, EnumStringField
#from pykson import TypeHierarchyAdapter

from ..models.wc_method import WCMethod
from ..models.session.wc_session_request import WCSessionRequest
from ..models.session.wc_session_update import WCSessionUpdate
from ..models.ethereum.wc_ethereum_transaction import WCEthereumTransaction
from ..models.ethereum.wc_ethereum_switch_chain import WCEthereumSwitchChain

JSONRPC_VERSION= "2.0"

class JsonRpcRequest(JsonObject):
    id_= IntegerField(serialized_name="id")
    jsonrpc = MultipleChoiceStringField(options=[JSONRPC_VERSION], null=False)
    method= EnumStringField(enum=WCMethod, null=True)
    #params= StringField #TODO

class JsonRpcRequest_SessionRequest(JsonRpcRequest):
    params= ObjectListField(WCSessionRequest)

class JsonRpcRequest_SessionUpdate(JsonRpcRequest):
    params= ObjectListField(WCSessionUpdate)
    
class JsonRpcRequest_EthSign(JsonRpcRequest):
    params= ListField(str)
    
class JsonRpcRequest_EthSignTransaction(JsonRpcRequest):
    params= ObjectListField(WCEthereumTransaction)

class JsonRpcRequest_SwitchEthereumChain(JsonRpcRequest):
    params= ObjectListField(WCEthereumSwitchChain)