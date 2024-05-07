import requests
import globals
import requests.exceptions
from middleware.proxy.utils.getProxy import getProxy
import loguru

def requestByProxy(url='https://www.google.com/'):
    # 持續更換代理直到連線請求成功為止
    while True:
        # 若無上一次連線請求成功的代理資訊，則重新取出一組代理資訊
        if globals.proxy is None:
            globals.proxy = getProxy()
        try:
            loguru.logger.info(f'requestByProxy: url is {url}')
            response = requests.get(
                url,
                # 指定 HTTPS 代理資訊
                proxies={
                    'https': f'https://{globals.proxy}'
                },
                # 指定連限逾時限制
                timeout=5
            )
            if response.status_code != 200:
                loguru.logger.debug(f'requestByProxy: status code is not 200.')
                # 請求發生錯誤，清除代理資訊，繼續下個迴圈
                globals.proxy = None
                continue
            loguru.logger.success(f'requestByProxy: downloaded.')
        # 發生以下各種例外時，清除代理資訊，繼續下個迴圈
        except requests.exceptions.ConnectionError:
            loguru.logger.error(f'requestByProxy: proxy({globals.proxy}) is not working (connection error).')
            globals.proxy = None
            continue
        except requests.exceptions.ConnectTimeout:
            loguru.logger.error(f'requestByProxy: proxy({globals.proxy}) is not working (connect timeout).')
            globals.proxy = None
            continue
        except requests.exceptions.ProxyError:
            loguru.logger.error(f'requestByProxy: proxy({globals.proxy}) is not working (proxy error).')
            globals.proxy = None
            continue
        except requests.exceptions.SSLError:
            loguru.logger.error(f'requestByProxy: proxy({globals.proxy}) is not working (ssl error).')
            globals.proxy = None
            continue
        except Exception as e:
            loguru.logger.error(f'requestByProxy: proxy({globals.proxy}) is not working.')
            loguru.logger.error(e)
            globals.proxy = None
            continue
        # 成功完成請求，離開迴圈
        break