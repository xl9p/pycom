from dth import DTH
import time
import pycom
from machine import Pin

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
time.sleep(1)

result = th.read()

if result.is_valid():
    print(result.temperature)
    print(result.humidity)