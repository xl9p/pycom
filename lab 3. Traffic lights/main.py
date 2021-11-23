import pycom
import time
from machine import Pin
from machine import PWM
import utime


PLAYING = False
COUNT = 0
TIME_LAST_PRESS = utime.ticks_ms()

def buttonEventCallback(arg):
    global PLAYING
    global TIME_LAST_PRESS
    global COUNT

    time_difference = utime.ticks_ms() - TIME_LAST_PRESS
    if time_difference >= 1000:
        COUNT += 1
        TIME_LAST_PRESS = utime.ticks_ms()
        
        print("\nButton pressed " + str(COUNT) + " time(s), time since last " + str(time_difference) + "ms")

        if PLAYING == False:
            print("Currently not playing. Start playing...")
            PLAYING = True
        else:
            print("Music is already playing.")   
    else:
        time_left = 1000 - time_difference
        print("\nIgnored button press due to contact bounce. Time left for next press is " + str(time_left))
        return





# Pins
redLED_t = Pin("P10", mode=Pin.OUT) #Make GPIO P8 an output
yellowLED_t = Pin("P9", mode=Pin.OUT) #Make GPIO P9 an output
greenLED_t = Pin("P8", mode=Pin.OUT) #Make GPIO P10 an output

yellowLED_b = Pin("P7", mode=Pin.OUT)

redLED_p = Pin("P20", mode=Pin.OUT)
greenLED_p = Pin("P19", mode=Pin.OUT)

buttonPin = Pin("P11", mode=Pin.IN, pull=None) # Make GPIO P11 an input
buzzer = Pin("P6") # Make GPIO P6 an output


buttonPin.callback(Pin.IRQ_FALLING, buttonEventCallback)

while True:
    if PLAYING == True:
        redLED_t.value(1)
        yellowLED_t.value(1)
        greenLED_t.value(1)
        time.sleep(2)
        redLED_t.value(0)
        yellowLED_t.value(0)
        greenLED_t.value(0)

        yellowLED_b.value(1)
        greenLED_p.value(1)
        redLED_p.value(1)
        time.sleep(2)
        yellowLED_b.value(0)
        greenLED_p.value(0)
        redLED_p.value(0)
        PLAYING == False