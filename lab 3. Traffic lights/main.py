import pycom
import time
from machine import Pin
from machine import PWM
import utime


BUTTON_PRESSED = False
TIME_LAST_PRESS = 0
E7 = 2637

def buttonEventCallback(arg):
    global BUTTON_PRESSED
    global TIME_LAST_PRESS

    time_last_press_diff = utime.ticks_ms() - TIME_LAST_PRESS
    if time_last_press_diff >= 1000:
        TIME_LAST_PRESS = utime.ticks_ms()
        print("\nButton pressed " + " time(s), time since last " + str(time_last_press_diff) + "ms")

        if BUTTON_PRESSED == False:
            BUTTON_PRESSED = True
            print("Button pressed.")
        else:
            print("Button pressed again, ignoring")  
    else:
        time_left = 1000 - time_last_press_diff
        print("\nIgnored button press due to contact bounce. Time left for next press is " + str(time_left))
        return


def Traffic_Go(g_t, y_t, r_t, r_p):
    print("\nTraffic is allowed to go, do not cross the road.")
    r_p.value(1)
    g_t.value(1)
    y_t.value(0)
    r_t.value(0)
    time.sleep(4)

def Pedestrian_Go(g_p, r_p):
    print("\nTraffic is not allowed to go, you can cross the road.")
    g_p.value(1)
    r_p.value(0)

    Use_Buzzer(5000, "fast")

def All_Stop(g_t, y_t, r_t, r_p, g_p):
    print("\nNo one is allowed to cross.")
    g_t.value(0)
    y_t.value(0)
    r_t.value(1)
    r_p.value(1)
    g_p.value(0)
    time.sleep(1)

def Traffic_Soon_Stop(g_t, y_t, r_t, r_p, g_p):
    print("\nTraffic soon will be stopped.")
    g_t.value(0)
    y_t.value(1)
    r_t.value(0)
    r_p.value(1)
    g_p.value(0)
    time.sleep(1)

def Traffic_Soon_Go(g_t, y_t, r_t, r_p, g_p):
    global BUTTON_PRESSED

    print("\nTraffic will be allowed to go soon, do not cross the road.")
    g_t.value(0)
    y_t.value(1)
    r_t.value(1)
    r_p.value(1)
    g_p.value(0)
    time.sleep(1)
    BUTTON_PRESSED = False


def Pedestrian_Soon_Stop(g_t, y_t, r_t, r_p, g_p):
    print("\nTraffic will be allowed to go soon, finish crossing the road.")
    g_t.value(0)
    y_t.value(1)
    r_t.value(1)
    r_p.value(0)
    g_p.value(1)

    Use_Buzzer(5000, "slow")

def Yellow_Button_On(y_b):
    y_b.value(1)

def Yellow_Button_Off(y_b):
    y_b.value(0)
 
def Use_Buzzer(timer, speed):
    time_start = utime.ticks_ms()
    interval = 0

    tim = PWM(0, frequency=300)
    ch = tim.channel(2, duty_cycle=0.5, pin=p2)

    if speed == "slow":
        interval = 0.30
    elif speed == "fast":
        interval = 0.15

    while True:
        time_diff = utime.ticks_ms() - time_start
        if time_diff >= timer:
            ch.duty_cycle(0)
            break
        tim = PWM(0, frequency=1568)
        ch.duty_cycle(0.5)
        time.sleep(interval)
        ch.duty_cycle(0)

# Pins
redLED_t = Pin("P10", mode=Pin.OUT) #Make GPIO P8 an output
yellowLED_t = Pin("P9", mode=Pin.OUT) #Make GPIO P9 an output
greenLED_t = Pin("P8", mode=Pin.OUT) #Make GPIO P10 an output

yellowLED_b = Pin("P7", mode=Pin.OUT)

redLED_p = Pin("P21", mode=Pin.OUT)
greenLED_p = Pin("P20", mode=Pin.OUT)

buttonPin = Pin("P11", mode=Pin.IN, pull=None) # Make GPIO P11 an input
p2 = Pin("P6") # Make GPIO P6 an output


buttonPin.callback(Pin.IRQ_FALLING, buttonEventCallback)

while True:
    if BUTTON_PRESSED == True:
        Yellow_Button_On(yellowLED_b)
        Traffic_Soon_Stop(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
        All_Stop(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
        Yellow_Button_Off(yellowLED_b)
        Pedestrian_Go(greenLED_p, redLED_p)
        Pedestrian_Soon_Stop(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
        Traffic_Soon_Go(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)        
    Traffic_Go(greenLED_t, yellowLED_t, redLED_t, redLED_p)
