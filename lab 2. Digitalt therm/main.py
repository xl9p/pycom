import time
from machine import Pin
from dth import DTH


th = DTH('P11', 0)
time.sleep(5)
result = th.read()
if result.is_valid():
    print("Temperature: " + str(result.temperature)+"C")
    print("Humidity: " + str(result.humidity)+"%")