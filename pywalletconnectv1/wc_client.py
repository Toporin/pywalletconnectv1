import logging
import websocket
import ssl
import certifi
import threading
import uuid
import time
from typing import List
from urllib.parse import unquote, urlparse, parse_qs
from pykson import Pykson #, JsonObject, IntegerField, StringField, ObjectListField

from pywalletconnectv1.wc_cipher import WCCipher
from pywalletconnectv1.models.wc_method import WCMethod
from pywalletconnectv1.models.wc_account import WCAccount
from pywalletconnectv1.models.wc_peer_meta import WCPeerMeta
from pywalletconnectv1.models.wc_socket_message import WCSocketMessage, MessageType
from pywalletconnectv1.models.wc_encryption_payload import WCEncryptionPayload
from pywalletconnectv1.models.session.wc_session import WCSession
from pywalletconnectv1.models.session.wc_session_update import WCSessionUpdate
from pywalletconnectv1.models.session.wc_approve_session_response import WCApproveSessionResponse
from pywalletconnectv1.jsonrpc.json_rpc_response import JsonRpcErrorResponse, JsonRpcResponse, JsonRpcResponse_ApproveSession, JsonRpcResponse_ResultString, JsonRpcResponse_ResultNone
from pywalletconnectv1.jsonrpc.json_rpc_error import JsonRpcError
from pywalletconnectv1.jsonrpc.json_rpc_request import JsonRpcRequest, JsonRpcRequest_SessionRequest, JsonRpcRequest_SessionUpdate, JsonRpcRequest_EthSign, JsonRpcRequest_EthSignTransaction, JsonRpcRequest_SwitchEthereumChain
from pywalletconnectv1.models.ethereum.wc_ethereum_sign_message import WCEthereumSignMessage, WCSignType

logger = logging.getLogger(__name__)

JSONRPC_VERSION = "2.0"
WS_CLOSE_NORMAL = 1000

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())
ssl_opts={'context': ssl_context}

class WCClient:
    
    def __init__(self):
        self.cipher= WCCipher()
        self.socket= None
        self.listeners= []
        self.session= None
        self.peerMeta= None
        self.peerId= None
        self.remotePeerId= None
        self.chainId= None
        self.isConnected= False
        self.handshakeId=-1
        
        self.wc_callback= None # external object that will execute requests
    
    # def onFailure(self): 
        # pass
    # def onDisconnect(code: int, reason: str):
        # pass
    # def onSessionRequest: (id: int, peer: WCPeerMeta):
        # pass
    # def onEthSign: (id: int, message: WCEthereumSignMessage):
        # pass
    # def onEthSignTransaction: (id: int, transaction: WCEthereumTransaction):
        # pass
    # def onEthSendTransaction: (id: int, transaction: WCEthereumTransaction):
        # pass
    # def onCustomRequest: (id: int, payload: String):
        # pass
    # def onBnbTrade: (id: int, order: WCBinanceTradeOrder):
    # def onBnbCancel: (id: int, order: WCBinanceCancelOrder):
        # pass
    # def onBnbTransfer: (id: int, order: WCBinanceTransferOrder):
        # pass
    # def onBnbTxConfirm: (id: int, order: WCBinanceTxConfirmParam):
        # pass
    # def onGetAccounts: (id: int):
        # pass
    # def onSignTransaction: (id: int, transaction: WCSignTransaction):
        # pass
        
    def set_callback(self, wc_callback):
        self.wc_callback= wc_callback
    

    def on_open(self, ws):
        logger.info("<< websocket opened >>")
        self.isConnected = True

        # self.listeners.forEach { it.onOpen(webSocket, response) }

        # val session = this.session ?: throw IllegalStateException("session can't be null on connection open")
        # val peerId = this.peerId ?: throw IllegalStateException("peerId can't be null on connection open")
        
        # The Session.topic channel is used to listen session request messages only.
        self.subscribe(self.session.topic)
        # The peerId channel is used to listen to all messages sent to this httpClient.
        self.subscribe(self.peerId)
    
    def on_message(self,  ws, text: str):
        logger.info(f"on_message START")
        decrypted=""
        try:
            logger.info(f"<== message {text}")
            decrypted = self.decryptMessage(text)
            logger.info(f"<== decrypted {decrypted}")
            self.handleMessage(decrypted)
        except Exception as e:
            self.wc_callback.onFailure(e)
        finally:
            #listeners.forEach { it.onMessage(webSocket, decrypted ?: text) }
            # TODO
            pass
    
    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, *args):
        logger.info('Websocket Closed')

    def on_heartbeat(self, args):
        logger.debug(args)

    
    def connect(self, session: WCSession, peerMeta: WCPeerMeta, peerId: str = None, remotePeerId: str = None):
        logger.info(f"connect - START")
        
        if (self.session != None and self.session.topic != session.topic):
            self.killSession()

        self.session = session
        self.peerMeta = peerMeta
        if peerId is None:
            self.peerId = str(uuid.uuid4())  # random uuid
        else:
            self.peerId = peerId
        self.remotePeerId = remotePeerId
        logger.info(f"connect - peerId: {self.peerId}")
        # val request = Request.Builder()
            # .url(session.bridge)
            # .build()
        #socket = httpClient.newWebSocket(request, self)
        
        #socket = websocket.WebSocket()
        #websocket.enableTrace(True)
        self.socket = websocket.WebSocketApp(self.session.bridge, 
                                                on_open= self.on_open,
                                                on_message=self.on_message,
                                                on_error= self.on_error)
        #self.socket.run_forever() # TODO: non-blocking!
        self.wst = threading.Thread(target=self.socket.run_forever, kwargs={'sslopt':ssl_opts})
        self.wst.daemon = True
        self.wst.start()
        logger.info(f"connect - END")
        
    
    def approveSession(self, accounts: List[str], chainId: int) -> bool:
        logger.info(f"DEBUG approveSession START")
        #check(handshakeId > 0) { "handshakeId must be greater than 0 on session approve" } # TODO
        self.chainId = chainId #str(chainId)
        result = WCApproveSessionResponse(
            approved= True,
            chainId = chainId,
            accounts = accounts,
            peerId = self.peerId,
            peerMeta = self.peerMeta
        )
        #result= Pykson().to_json(result)
        #logger.info(f"DEBUG approveSession result_str= {result}")
        response = JsonRpcResponse_ApproveSession(
            jsonrpc= JSONRPC_VERSION,
            id_ = self.handshakeId,
            result = result #result_str
        )
        json= Pykson().to_json(response)
        logger.info(f"DEBUG approveSession response= {json}")
        return self.encryptAndSend(json)
    
    def updateSession(self, accounts: List[str]= None, chainId: int=None, approved: bool = True) -> bool:
        if chainId is None:
            if self.chainId is not None:
                chainId= int(self.chainId) 

        request = JsonRpcRequest_SessionUpdate(
            jsonrpc= JSONRPC_VERSION,
            id_ = self.generateId(), 
            method = WCMethod.SESSION_UPDATE,
            params =    [WCSessionUpdate(
                                    approved = approved,
                                    chainId = chainId,
                                    accounts = accounts
                                )]
        )
        json= Pykson().to_json(request)
        return self.encryptAndSend(json)
    
    def rejectSession(self, message: str = "Session rejected") -> bool:
        #check(handshakeId > 0) { "handshakeId must be greater than 0 on session reject" } # TODO
        response = JsonRpcErrorResponse(
            jsonrpc= JSONRPC_VERSION,
            id_ = self.handshakeId,
            error = JsonRpcError(code= -32000, message = message)
        )
        json= Pykson().to_json(response)
        return self.encryptAndSend(json)
    
    def killSession(self) -> bool:
        self.updateSession(approved = False)
        return self.disconnect()
    
    def approveRequest(self, id_: int, result) -> bool:
        # ugly...
        if type(result) is str:
            response = JsonRpcResponse_ResultString(
                jsonrpc= JSONRPC_VERSION,
                id_ = id_,
                result = result 
            )
        elif type(result) is WCAccount:
            response = JsonRpcResponse_ResultWCAccount(
                jsonrpc= JSONRPC_VERSION,
                id_ = id_,
                result = result 
            )
        elif result is None:
            response = JsonRpcResponse_ResultNone(
                jsonrpc= JSONRPC_VERSION,
                id_ = id_,
                result = None
            )
        json= Pykson().to_json(response)
        return self.encryptAndSend(json)
    
    def rejectRequest(self, id_: int, message: str = "Reject by the user") -> bool:
        response = JsonRpcErrorResponse(
            jsonrpc= JSONRPC_VERSION,
            id_ = id_,
            error = JsonRpcError(code= -32000, message = message)
        )
        json= Pykson().to_json(response)
        return self.encryptAndSend(json)
    
    def decryptMessage(self, text: str) -> str:
        #message = gson.fromJson<WCSocketMessage>(text)
        message= Pykson().from_json(text, WCSocketMessage, accept_unknown=True)
        encrypted= Pykson().from_json(message.payload, WCEncryptionPayload)
        
        #val encrypted = gson.fromJson<WCEncryptionPayload>(message.payload)
        #val session = this.session ?: throw IllegalStateException("session can't be null on message receive") #TODO
        decrypted_bytes= self.cipher.decrypt(encrypted, bytes.fromhex(self.session.key))
        decrypted_str= decrypted_bytes.decode('utf-8')
        return decrypted_str
        
    def invalidParams(self, id_: int) -> bool:
        response = JsonRpcErrorResponse(
            jsonrpc= JSONRPC_VERSION,
            id_ = id_,
            error = JsonRpcError(code=-32602, message=  "Invalid parameters")
        )
        json= Pykson().to_json(response)
        return self.encryptAndSend(json)
    
    def handleMessage(self, payload: str):
        try:
            request= Pykson().from_json(payload, JsonRpcRequest,  accept_unknown=True) # ignore param key
            try:
                method= request.method
                if method is not None:
                    self.handleRequest(payload, method)
                else:
                    logger.info(f"DEBUG in handleMessage - onCustomRequest - payload: {payload}")
                    self.wc_callback.onCustomRequest(request.id_, payload)
            except Exception as e:
                self.wc_callback.onFailure(e)
            except AttributeError:
                self.wc_callback.onCustomRequest(request.id_, payload) # TODO?
        except InvalidJsonRpcParamsException as e:
            self.invalidParams(e.requestId)
    
    def handleRequest(self, payload:str, method: str):
        logger.info(f"DEBUG in handleRequest - START - method= {method}")
        if method== WCMethod.SESSION_REQUEST.value:
            try:
                request= Pykson().from_json(payload, JsonRpcRequest_SessionRequest) # include param key
                param= request.params[0] # take the first of the list or throw
                logger.info(f"DEBUG in handleRequest - SESSION_REQUEST - param: {param}")
                self.handshakeId = request.id_
                self.remotePeerId = param.peerId
                self.chainId = param.chainId
                self.wc_callback.onSessionRequest(request.id_, param.peerMeta)
            except Exception as e:
                logger.warning(f"Exception in handleRequest - SESSION_REQUEST - {e}")
            
        elif method== WCMethod.SESSION_UPDATE.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_SessionUpdate, accept_unknown=True) # include param key # unknownfield:networkId
                param= request.params[0] # take the first of the list or throw
                logger.info(f"DEBUG in handleRequest - SESSION_UPDATE - param: {param}")
                if (not param.approved):
                    self.wc_callback.killSession()
            except Exception as e:
                logger.warning(f"Exception in handleRequest - SESSION_UPDATE - {e}")
        
        elif method== WCMethod.ETH_SIGN.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_EthSign) # include param key
                params= request.params 
                logger.info(f"DEBUG in handleRequest - ETH_SIGN - params: {params}")
                if len(params) < 2:
                    raise InvalidJsonRpcParamsException(request.id_)
                self.wc_callback.onEthSign(request.id_, WCEthereumSignMessage(raw=params, type_=WCSignType.MESSAGE))
            except Exception as e:
                    logger.warning(f"Exception in handleRequest - ETH_SIGN - {e}")
                    # todo
           
        elif method== WCMethod.ETH_PERSONAL_SIGN.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_EthSign) # include param key
                params= request.params 
                logger.info(f"DEBUG in handleRequest - ETH_PERSONAL_SIGN - params: {params}")
                if len(params) < 2:
                    raise InvalidJsonRpcParamsException(request.id_)
                self.wc_callback.onEthSign(request.id_, WCEthereumSignMessage(raw=params, type_=WCSignType.PERSONAL_MESSAGE))
            except Exception as e:
                    logger.warning(f"Exception in handleRequest - ETH_PERSONAL_SIGN - {e}")
                    # todo  
        
        elif method== WCMethod.ETH_SIGN_TYPE_DATA.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_EthSign) # include param key
                params= request.params 
                logger.info(f"DEBUG in handleRequest - ETH_SIGN_TYPE_DATA - params: {params}")
                if len(params) < 2:
                    raise InvalidJsonRpcParamsException(request.id_)
                self.wc_callback.onEthSign(request.id_, WCEthereumSignMessage(raw=params, type_=WCSignType.TYPED_MESSAGE))
            except Exception as e:
                    logger.warning(f"Exception in handleRequest - ETH_SIGN_TYPE_DATA - {e}")
                
        elif method== WCMethod.ETH_SIGN_TRANSACTION.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_EthSignTransaction) # include param key
                param= request.params[0] # take the first of the list or raise
                logger.info(f"DEBUG in handleRequest - ETH_SIGN_TRANSACTION - param: {param}")
                self.wc_callback.onEthSignTransaction(request.id_, param)
            except Exception as e:
                    logger.warning(f"Exception in handleRequest - ETH_SIGN_TRANSACTION - {e}")
        
        elif method== WCMethod.ETH_SEND_TRANSACTION.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_EthSignTransaction) # include param key
                param= request.params[0] # take the first of the list or raise
                logger.info(f"DEBUG in handleRequest - ETH_SEND_TRANSACTION - param: {param}")
                self.wc_callback.onEthSendTransaction(request.id_, param)
            except Exception as e:
                logger.warning(f"Exception in handleRequest - ETH_SEND_TRANSACTION - {e}")
        
        elif method== WCMethod.SWITCH_CHAIN.value:
            try: 
                request= Pykson().from_json(payload, JsonRpcRequest_SwitchEthereumChain) # include param key
                param= request.params[0] # take the first of the list or raise
                logger.info(f"DEBUG in handleRequest - SWITCH_CHAIN - param: {param}")
                self.wc_callback.onEthSwitchChain(request.id_, param)
            except Exception as e:
                logger.warning(f"Exception in handleRequest - SWITCH_CHAIN - {e}")
        
        else:   
            logger.warning(f"WARNING in handleRequest - unsupported method: {method} - payload: {payload}")
                    
                    
    def subscribe(self, topic: str) -> bool:
        logger.info(f"subscribe START")
        message = WCSocketMessage(
            topic = topic,
            type_ = MessageType.SUB,
            payload = ""
        )
        json = Pykson().to_json(message)
        logger.info(f"==> subscribe {json}")
        
        if self.socket is None:
            return False
        else:
            self.socket.send(json)
            logger.info(f"==> subscribe message sent!")
            return True

    def encryptAndSend(self, result: str) -> bool: 
        logger.info(f"==> encryptAndSend message {result}")
        # val session = this.session ?: throw IllegalStateException("session can't be null on message send")
        
        payload_obj= self.cipher.encrypt(result.encode("utf-8"), bytes.fromhex(self.session.key))
        payload= Pykson().to_json(payload_obj)
        
        #val payload = gson.toJson(WCCipher.encrypt(result.toByteArray(Charsets.UTF_8), session.key.hexStringToByteArray()))
        
        # Once the remotePeerId is defined, all messages must be sent to this channel. The session.topic channel
        # will be used only to respond the session request message.
        if self.remotePeerId is None:
            message = WCSocketMessage(
                topic = self.session.topic,
                type_ = MessageType.PUB,
                payload = payload
            )
        else:
            message = WCSocketMessage(
                topic = self.remotePeerId,
                type_ = MessageType.PUB,
                payload = payload
            )
        json = Pykson().to_json(message)
        logger.info(f"==> encrypted {json}")
        
        if self.socket is None:
            return False
        else:
            self.socket.send(json)
            return True


    def disconnect(self) -> bool:
        if self.socket is None:
            return False
        else:
            self.socket.close(status=WS_CLOSE_NORMAL)
            return True
    
    def generateId(self) -> int:
        #return int(time.time()) # with python>= 3.7: time.time_ns() or int(time.time()*10**9)?
        return int(time.time()*10**6) 
    
    def addSocketListener(self, listener): # TODO listener: WebSocketListener
        self.listeners.append(listener)

    def removeSocketListener(self, listener): # TODO listener: WebSocketListener
        self.listeners.remove(listener) # TODO
    
    def resetState(self):
        self.handshakeId = -1
        self.isConnected = False
        self.session = None
        self.peerId = None
        self.remotePeerId = None
        self.peerMeta = None
    
class InvalidJsonRpcParamsException(Exception):
    def __init__(self, requestId: int):            
        super().__init__("Invalid JSON RPC Request")
        self.requestId = requestId