from pykson import JsonObject, StringField, IntegerField, ListField, ObjectField, MultipleChoiceStringField, TypeHierarchyAdapter

from .json_rpc_error import JsonRpcError
from ..models.wc_account import WCAccount
from ..models.session.wc_approve_session_response import WCApproveSessionResponse

JSONRPC_VERSION= "2.0"

class JsonRpcErrorResponse(JsonObject):
    #val jsonrpc: String = JSONRPC_VERSION,
    jsonrpc = MultipleChoiceStringField(options=[JSONRPC_VERSION], null=False)
    id_= IntegerField(serialized_name="id")
    error= ObjectField(JsonRpcError)

class JsonRpcResponse(JsonObject):
    #jsonrpc: String = JSONRPC_VERSION,
    jsonrpc = MultipleChoiceStringField(options=[JSONRPC_VERSION], null=False)
    id_= IntegerField(serialized_name="id")
    #result= StringField() # TODO T template?

class JsonRpcResponse_ApproveSession(JsonRpcResponse):
    result= ObjectField(WCApproveSessionResponse)
    
class JsonRpcResponse_ResultString(JsonRpcResponse):
    result= StringField()

class JsonRpcResponse_ResultWCAccount(JsonRpcResponse):
    result= ObjectField(WCAccount)
