import pycom
import time
from machine import Pin
from machine import PWM
import utime


# Pins
redLED_t = Pin("P10", mode=Pin.OUT) #Make GPIO P8 an output
yellowLED_t = Pin("P9", mode=Pin.OUT) #Make GPIO P9 an output
greenLED_t = Pin("P8", mode=Pin.OUT) #Make GPIO P10 an output

yellowLED_b = Pin("P7", mode=Pin.OUT)

redLED_p = Pin("P20", mode=Pin.OUT)
greenLED_p = Pin("P19", mode=Pin.OUT)

buttonPin = Pin("P11", mode=Pin.IN, pull=None) # Make GPIO P11 an input
buzzer = Pin("P6") # Make GPIO P6 an output