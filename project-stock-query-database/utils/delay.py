import random
import time

def delay():
    random_delay = random.randint(3, 10)
    print('等待', random_delay, '秒後進行下一次請求...')
    time.sleep(random_delay)