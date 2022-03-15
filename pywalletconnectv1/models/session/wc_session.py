import logging
from urllib.parse import unquote, urlparse, parse_qs
from pykson import JsonObject, StringField

logger = logging.getLogger(__name__)

class WCSession(JsonObject):
    topic= StringField()
    version= StringField()
    bridge= StringField()
    key= StringField()
    
    @classmethod
    def from_uri(cls, wcurl:str):
        try:   
            logger.info("wcurl: " + wcurl)
            # remove service name
            wcurl_splitted= wcurl.split("wc?uri=")
            wcurl= wcurl_splitted[-1]
            logger.info("wcurl_trimmed: " + wcurl)
            
            # url decode 
            wcurl_dec = unquote(wcurl)
            wcurl_dec = unquote(wcurl_dec)
            logger.info(f"wcurl_dec: {wcurl_dec}")
            
            # parse
            wcurl_dec= wcurl_dec.replace('wc:', 'wc://')
            wcurl_parsed= urlparse(wcurl_dec)
            logger.info(f"wcurl_parsed: {wcurl_parsed}")
            
            wcurl_query= wcurl_parsed.query
            logger.info(f"wcurl_query: {wcurl_query}")
            
            query_parsed= parse_qs(wcurl_query)
            bridge= query_parsed['bridge'][0]
            bridge= bridge.replace("https://", "wss://") # TODO?
            logger.info(f"bridge: {bridge}")
            key= query_parsed['key'][0]
            logger.info(f"key: {key}")

            netloc= wcurl_parsed.netloc
            netloc_split= netloc.split('@')
            topic= netloc_split[0]
            version= netloc_split[1]
            logger.info(f"topic: {topic}")
            logger.info(f"version: {version}")
            
            return cls(topic= topic, version= version, bridge= bridge, key= key)
            
        except Exception as ex:
            logger.info(f"Exception in WCSession: {ex}")
            raise ValueError(f"Exception while parsing WalletConnect URL: {ex}")
    
    #def __init__(self, wcurl:str):
        # self.topic: str= None
        # self.version: str= None
        # self.bridge: str= None
        # self.key: str= None
        # try:   
            # logger.info("wcurl: " + wcurl)
            # # remove service name
            # wcurl_splitted= wcurl.split("wc?uri=")
            # wcurl= wcurl_splitted[-1]
            # logger.info("wcurl_trimmed: " + wcurl)
            
            # # url decode 
            # wcurl_dec = unquote(wcurl)
            # wcurl_dec = unquote(wcurl_dec)
            # logger.info(f"wcurl_dec: {wcurl_dec}")
            
            # # parse
            # wcurl_dec= wcurl_dec.replace('wc:', 'wc://')
            # wcurl_parsed= urlparse(wcurl_dec)
            # logger.info(f"wcurl_parsed: {wcurl_parsed}")
            
            # wcurl_query= wcurl_parsed.query
            # logger.info(f"wcurl_query: {wcurl_query}")
            
            # query_parsed= parse_qs(wcurl_query)
            # self.bridge= query_parsed['bridge'][0]
            # self.bridge= self.bridge.replace("https://", "wss://") # TODO?
            # logger.info(f"bridge: {self.bridge}")
            # self.key= query_parsed['key'][0]
            # logger.info(f"key: {self.key}")

            # netloc= wcurl_parsed.netloc
            # netloc_split= netloc.split('@')
            # self.topic= netloc_split[0]
            # self.version= netloc_split[1]
            # logger.info(f"topic: {self.topic}")
            # logger.info(f"version: {self.version}")
            
        # except Exception as ex:
            # logger.info(f"Exception in WCSession: {ex}")
            # raise ValueError(f"Exception while parsing WalletConnect URL: {ex}")
        
    def to_uri(self) -> str:
        return  f"wc:{self.topic}@{self.version}?bridge={self.bridge}&key={self.key}"
    