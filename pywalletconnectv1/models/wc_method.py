from enum import Enum

class WCMethod(Enum):
    SESSION_REQUEST= "wc_sessionRequest"
    SESSION_UPDATE= "wc_sessionUpdate"
    ETH_SIGN= "eth_sign"
    ETH_PERSONAL_SIGN= "personal_sign"
    ETH_SIGN_TYPE_DATA= "eth_signTypedData"
    ETH_SIGN_TRANSACTION= "eth_signTransaction"
    ETH_SEND_TRANSACTION= "eth_sendTransaction"
    BNB_SIGN= "bnb_sign"
    BNB_TRANSACTION_CONFIRM= "bnb_tx_confirmation"
    GET_ACCOUNTS= "get_accounts"
    SIGN_TRANSACTION= "trust_signTransaction"
    SWITCH_CHAIN= "wallet_switchEthereumChain"