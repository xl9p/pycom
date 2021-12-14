from machine import Pin, I2C
from bmp085 import BMP180

i2c = I2C(0, I2C.MASTER, baudrate=20000)
bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 101325

temp = bmp.temperature
p = bmp.pressure
altitude = bmp.altitude
print(temp, p, altitude)