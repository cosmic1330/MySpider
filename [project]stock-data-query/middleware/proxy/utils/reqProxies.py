from middleware.proxy.nova import getProxiesFromProxyNova
from middleware.proxy.freeProxyList import getProxiesFromFreeProxyList
from loguru import logger

def reqProxies():
    proxies = []
    proxies = proxies + getProxiesFromFreeProxyList()
    proxies = proxies + getProxiesFromProxyNova()
    proxies = list(dict.fromkeys(proxies))
    logger.debug(f'reqProxies: {len(proxies)} proxies is found.')
    return proxies