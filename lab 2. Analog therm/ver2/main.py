import time
import machine
import math


adc = machine.ADC(bits=12)
apin = adc.channel(pin='P16', attn=adc.ATTN_0DB)

print(str(apin.voltage()))