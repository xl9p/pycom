import time
import machine
import math

R1 = 10000
VREF = 3.3
MAX_DC_VALUE = 4096
A, B, C = 0.001129148, 0.000234125, 0.0000000876741 # Steinharts A, B, C constants from manufact. 


def ThermistorRes(raw_adc):
    mVol = (raw_adc / MAX_DC_VALUE) * VREF
    return ((R1 * VREF) / mVol) - R1

def CalculateTemp(t_res):
    return 1 / (A + B*(math.log(t_res)) + C*(math.log(t_res))**3) - 273.15


adc = machine.ADC(bits=12)
apin = adc.channel(pin='P16', attn=adc.ATTN_11DB)


while True:
    raw_adc = apin.value()
    t_res = ThermistorRes(raw_adc)
    temp = CalculateTemp(t_res)
    print("Temperature: " + str(round(temp, 2)) + "C")
    time.sleep(2)