
import globals
import random
from middleware.proxy.utils.getProxies import getProxies
import loguru

def getProxy():
    # 若代理清單內已無代理，則重新下載
    if len(globals.proxies) == 0:
        getProxies()
    proxy = random.choice(globals.proxies)
    loguru.logger.debug(f'getProxy: {proxy}')
    globals.proxies.remove(proxy)
    loguru.logger.debug(f'getProxy: {len(globals.proxies)} proxies is unused.')
    return proxy