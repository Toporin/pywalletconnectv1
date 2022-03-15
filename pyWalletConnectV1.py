import json
import threading
import time
import logging
import sys
import os.path
import uuid

from urllib.parse import unquote, urlparse, parse_qs
#from websocket import create_connection
import websocket

from wc_callback import WCCallback
from pywalletconnectv1.wc_cipher import WCCipher
from pywalletconnectv1.wc_client import WCClient
from pywalletconnectv1.models.wc_peer_meta import WCPeerMeta
from pywalletconnectv1.models.session.wc_session import WCSession


if (len(sys.argv)>=2) and (sys.argv[1]in ['-v', '--verbose']):
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s [%(module)s] %(funcName)s | %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(module)s] %(funcName)s | %(message)s')
logger = logging.getLogger(__name__)
logger.warning("loglevel: "+ str(logger.getEffectiveLevel()) )


wc_url = input("Enter wc url: ")
logger.info("wc_url: " + wc_url)

wc_session= WCSession(wc_url)
wc_peer_meta = WCPeerMeta(name = "Satochip-Bridge", url = "https://satochip.io", description="Satochip - the open-source and affordable hardware wallet!")

wc_client= WCClient()
wc_callback= WCCallback(wc_client, None, None)
wc_client.set_callback(wc_callback)

# handle session
wc_client.connect(wc_session, wc_peer_meta)
