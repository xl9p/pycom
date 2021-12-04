import time
from machine import Pin
from dth import DTH
import machine
import math

R1 = 10000
VREF = 3.3
# Since we're using 12 bits in order to convert analogue signal to bits, the max value is 4096 (max voltage)
# If we were using 9 bits it would be 512, 10 bits 1023, 12 bits 4096
MAX_DC_VALUE = 4096
A, B, C = 0.001129148, 0.000234125, 0.0000000876741 # Steinhart-Hart's A, B, C constants from manufact. 


def ThermistorRes(raw_adc):
    mVol = (raw_adc / MAX_DC_VALUE) * VREF
    return ((R1 * VREF) / mVol) - R1 # calculating resistance for thermistor

def CalculateTemp(t_res):
    # calculating temperature using Steinhart-Hart's equation https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation
    temp_k = 1 / (A + B*(math.log(t_res)) + C*(math.log(t_res))**3)
    temp_c = temp_k - 273.15
    return temp_c

adc = machine.ADC(bits=10)
apin = adc.channel(pin='P16', attn=adc.ATTN_11DB)

th = DTH('P11', 0)

while True:
    print("\nDigital sensor's data:")
    result = th.read()
    if result.is_valid():
        print("Results are valid.")
        print("Temperature: " + str(result.temperature)+"C")
        print("Humidity: " + str(result.humidity)+"%")
    else:
        print("Results may be not valid.")
        print("Temperature: " + str(result.temperature)+"C")
        print("Humidity: " + str(result.humidity)+"%")

    print("\nThermistor's data:")
    raw_adc = apin.value()
    t_res = ThermistorRes(raw_adc)
    temp = CalculateTemp(t_res)
    print("Temperature: " + str(round(temp, 2)) + "C")
    time.sleep(3)