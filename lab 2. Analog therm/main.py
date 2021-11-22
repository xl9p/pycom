import time
import machine
import math


adc = machine.ADC(bits=12)
apin = adc.channel(pin='P16')
print(str(apin.value()))
print(str(apin()))
m_vol = apin.voltage()


vol = m_vol / 1000
res_bal = 10000
beta = 3950*10**3
vol_src = 3.3

res = 10000 * ((vol_src / vol) - 1)
#res_bal * (3.3 / vol - 1)


temp_k = (beta * 25) / (beta + (25 * math.log(res / 25)))
temp_c = temp_k - 273.15

print("Resistance: " + str(res))
print("Voltage(mV): " + str(m_vol))
print("Voltage(v): " + str(vol))
print("Temp: " + str(temp_c))

apin.deinit()