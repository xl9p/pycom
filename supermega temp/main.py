from machine import Pin, I2C
from bmp085 import BMP180


print("test")
i2c = I2C()
bmp = BMP180(i2c)
bmp.oversample = 3
bmp.sealevel = 1013.25

while True:
    temp = bmp.temperature
    p = bmp.pressure
    altitude = bmp.altitude
    print(temp, p, altitude)