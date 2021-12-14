import time
from machine import Pin, ADC
import machine

#adc = machine.ADC()           
#apin = adc.channel(pin='P16')
#val = apin() 

VibSensorPin = 'P16' # sensor connected to P16. Valid pins are P13 to P20.
Pin(VibSensorPin, mode=Pin.IN)  # set up pin mode to input
adc = ADC(bits=10)             # create an ADC object bits=10 means range 0-705 the lower value the more vibration detected
apin = adc.channel(attn=ADC.ATTN_11DB, pin=VibSensorPin)
