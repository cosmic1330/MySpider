import csv
import datetime
import os
import random
import loguru
import globals
from middleware.proxy.utils.reqProxies import reqProxies

def getProxies():
    filename = f'{globals.EntryPoint}/proxies.csv'
    filepath = f'{filename}'
    if os.path.isfile(filepath):
        loguru.logger.info(f'getProxies: {filename} exists.')
        loguru.logger.warning(f'getProxies: {filename} is loading...')
        with open(filepath, 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                proxy = row['Proxy']
                globals.proxies.append(proxy)
        loguru.logger.success(f'getProxies: {filename} is loaded.')
    else:
        loguru.logger.info(f'getProxies: {filename} does not exist.')
        globals.proxies = reqProxies()
        loguru.logger.warning(f'getProxies: {filename} is saving...')
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Proxy'
            ])
            for proxy in globals.proxies:
                writer.writerow([
                    proxy
                ])
        loguru.logger.success(f'getProxies: {filename} is saved.')