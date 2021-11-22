import pycom
import time
from machine import Pin
from machine import PWM
import utime


PLAYING = False
COUNT = 0
TIME_LAST_PRESS = utime.ticks_ms()

E7 = 2637
F7 = 2794
C7 = 2093
G7 = 3136
G6 = 1568
E6 = 1319
A6 = 1760
B6 = 1976
AS6 = 1865
A7 = 3520
D7 = 2349


red_led_tones = [2637, 2794, 2093, 3136]
yellow_led_tones = [1568, 1319, 1760, 1976]
green_led_tones = [1865, 3520, 2349]


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

def playNotes(notes, r, y, g):
    global PLAYING

    tim = PWM(0, frequency=300)
    ch = tim.channel(2, duty_cycle=0.5, pin=p2)
    for i in notes:
        if i == 0:
            ch.duty_cycle(0)
        else:
            freq_to_led(i, r, y, g)
            tim = PWM(0, frequency=i)
            ch.duty_cycle(0.5)
        time.sleep(0.15)
    PLAYING = False

def freq_to_led(freq, r, y, g):
    r.value(0)
    y.value(0)
    g.value(0)
    if freq in red_led_tones:
        r.value(1)
    elif freq in yellow_led_tones:
        y.value(1)
    elif freq in green_led_tones:
        g.value(1)


print("Lab 2. Speaker")

# Pins
redLED = Pin("P8", mode=Pin.OUT) #Make GPIO P8 an output
yellowLED = Pin("P9", mode=Pin.OUT) #Make GPIO P9 an output
greenLED = Pin("P10", mode=Pin.OUT) #Make GPIO P10 an output
buttonPin = Pin("P11", mode=Pin.IN, pull=None) # Make GPIO P11 an input
p2 = Pin("P6") # Make GPIO P6 an output

# Mario notes
mario = [E7, E7, 0, E7, 0, C7, E7, 0, G7, 0, 0, 0, G6, 0, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0, C7, 0, 0, G6, 0, 0, E6, 0, 0, A6, 0, B6, 0, AS6, A6, 0, G6, E7, 0, G7, A7, 0, F7, G7, 0, E7, 0,C7, D7, B6, 0, 0]


# Main code
buttonPin.callback(Pin.IRQ_FALLING, buttonEventCallback)
while True:
    if PLAYING == True:
        playNotes(mario, redLED, yellowLED, greenLED)
