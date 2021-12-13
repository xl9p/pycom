from machine import Pin
import time


pin = Pin("P11", mode=Pin.IN, pull=None)

while True:
    print("vibration sensor data")
    print(str(pin()))

    time.sleep(3)