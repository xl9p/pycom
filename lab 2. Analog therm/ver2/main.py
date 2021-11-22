import time
import machine
import math


BETA = 3950
AMB_TEMP_K = 298.15
R1 = 100
VREF = 3.3
RES_AT_AMB_TEMP = 103
MAX_ADC_VALUE = 1023


def ThermistorRes(raw_adc):
    return R1 * 1/((MAX_ADC_VALUE/raw_adc) - 1)
    #return R1 * ( (MAX_ADC_VALUE / raw_adc) - 1)

def CalculateTemp(t_res):
    temp_k = (BETA * AMB_TEMP_K) / (BETA + (AMB_TEMP_K * math.log(t_res / RES_AT_AMB_TEMP)))
    return temp_k - 273.15

adc = machine.ADC(bits=10)
apin = adc.channel(pin='P16', attn=adc.ATTN_0DB)

while True:
    raw_adc = apin.value()
    t_res = ThermistorRes(raw_adc)
    temp = CalculateTemp(t_res)
    print("Temperature: " + str(round(temp, 2)) + "C")
    time.sleep(2)