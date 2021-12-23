from mqtt import MQTTClient_lib
from network import WLAN
import time
from machine import Pin
from machine import PWM
import utime
import machine


BUTTON_PRESSED = False
COUNT = 1
TIME_LAST_PRESS = utime.ticks_ms()
TIME_LAST_GREEN = utime.ticks_ms()
E7 = 2637
MQQT_ISCONNECTED = False
CLIENT = None

def wlan_connect(name, passw, wlan_obj):
    wlan_obj.connect(ssid=str(name), auth=(WLAN.WPA2, str(passw))) #smwm7221

    while not wlan_obj.isconnected():
        machine.idle()

    print("connected")
    return wlan_obj

def mqqt_connect(device, ipaddr, port):
    global MQQT_ISCONNECTED
    global CLIENT

    CLIENT = MQTTClient_lib(str(device), str(ipaddr), port=int(port))
    CLIENT.connect()
    print("MQTT connected")
    MQQT_ISCONNECTED = True

def buttonEventCallback(arg):
    global BUTTON_PRESSED
    global TIME_LAST_PRESS
    global TIME_LAST_GREEN

    time_last_press_diff = utime.ticks_ms() - TIME_LAST_PRESS
    if time_last_press_diff >= 1000:
        TIME_LAST_PRESS = utime.ticks_ms()

        time_diff = utime.ticks_ms() - TIME_LAST_GREEN
        if BUTTON_PRESSED == False and time_diff >= 3800:
            BUTTON_PRESSED = True
            print("Button pressed.")
        else:
            print("Button pressed again, ignoring")  
    else:
        return

def Traffic_Go(g_t, y_t, r_t, r_p):
    global COUNT
    r_p.value(1)
    g_t.value(1)
    y_t.value(0)
    r_t.value(0)
    
    if COUNT == 1:
        CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="1")
        time.sleep(0.2)
        CLIENT.publish(topic="is222zf/feeds/lights/traffic/", msg="GREEN")
        CLIENT.publish(topic="is222zf/feeds/lights/pedestrian/", msg="RED")

        CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="0")
    COUNT += 1

def Pedestrian_Go(g_p, r_p):
    print("\nTraffic is not allowed to go, you can cross the road.")
    print("Traffic: red")
    print("Pedestrian: green")
    print("Fast ticks")
    g_p.value(1)
    r_p.value(0)
    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="1")
    time.sleep(0.2)
    CLIENT.publish(topic="is222zf/feeds/lights/traffic/", msg="RED")
    CLIENT.publish(topic="is222zf/feeds/lights/pedestrian/", msg="GREEN")

    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="0")
    Use_Buzzer(2800, "fast")
    
def All_Stop(g_t, y_t, r_t, r_p, g_p):
    print("\nNo one is allowed to cross.")
    print("Traffic: red")
    print("Pedestrian: red")
    g_t.value(0)
    y_t.value(0)
    r_t.value(1)
    r_p.value(1)
    g_p.value(0)
    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="1")
    time.sleep(0.2)
    CLIENT.publish(topic="is222zf/feeds/lights/traffic/", msg="RED")
    CLIENT.publish(topic="is222zf/feeds/lights/pedestrian/", msg="RED")
    
    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="0")
    time.sleep(0.8)

def Traffic_Soon_Stop(g_t, y_t, r_t, r_p, g_p):
    print("\nTraffic soon will be stopped.")
    print("Traffic: yellow")
    print("Pedestrian: red")
    g_t.value(0)
    y_t.value(1)
    r_t.value(0)
    r_p.value(1)
    g_p.value(0)

    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="1")
    time.sleep(0.2)
    CLIENT.publish(topic="is222zf/feeds/lights/traffic/", msg="YELLOW")
    CLIENT.publish(topic="is222zf/feeds/lights/pedestrian/", msg="RED")

    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="0")
    time.sleep(1.8)

def Traffic_Soon_Go(g_t, y_t, r_t, r_p, g_p):
    global BUTTON_PRESSED
    global TIME_LAST_GREEN
    global COUNT

    print("\nTraffic will be allowed to go soon, do not cross the road.")
    print("Traffic: yellow, red")
    print("Pedestrian: red")
    g_t.value(0)
    y_t.value(1)
    r_t.value(1)
    r_p.value(1)
    g_p.value(0)

    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="1")
    time.sleep(0.2)
    CLIENT.publish(topic="is222zf/feeds/lights/traffic/", msg="YELLOW, RED")
    CLIENT.publish(topic="is222zf/feeds/lights/pedestrian/", msg="RED")

    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="0")
    time.sleep(0.8)

    TIME_LAST_GREEN = utime.ticks_ms()
    BUTTON_PRESSED = False
    COUNT = 1

def Pedestrian_Soon_Stop(g_t, y_t, r_t, r_p, g_p):
    print("\nTraffic will be allowed to go soon, finish crossing the road.")
    print("Traffic: red")
    print("Pedestrian: green")
    print("Slow ticks")
    g_t.value(0)
    y_t.value(0)
    r_t.value(1)
    r_p.value(0)
    g_p.value(1)
    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="1")
    time.sleep(0.2)
    CLIENT.publish(topic="is222zf/feeds/lights/traffic/", msg="RED")
    CLIENT.publish(topic="is222zf/feeds/lights/pedestrian/", msg="GREEN")

    CLIENT.publish(topic="is222zf/feeds/lights/issending/", msg="0")
    Use_Buzzer(800, "slow")

def Yellow_Button_On(y_b):
    y_b.value(1)

def Yellow_Button_Off(y_b):
    y_b.value(0)
 
def Use_Buzzer(timer, speed):
    time_start = utime.ticks_ms()
    interval = 0

    tim = PWM(0, frequency=300)
    ch = tim.channel(2, duty_cycle=0.3, pin=p2)

    if speed == "slow":
        interval = 0.45
    elif speed == "fast":
        interval = 0.15

    while True:
        time_diff = utime.ticks_ms() - time_start
        if time_diff >= timer:
            ch.duty_cycle(0)
            break
        tim = PWM(0, frequency=1568)
        ch.duty_cycle(0.3)
        time.sleep(interval)
        ch.duty_cycle(0)



print("Lab 3. Traffic lights, sending")

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


wlan = WLAN(mode=WLAN.STA)

while True:
    try:
        if not wlan.isconnected():
            print("\nNot connected to WLAN, trying to connect in 1 second")
            time.sleep(1)
            wlan = wlan_connect("Galaxy S96a30", "smwm7221", wlan)
        elif not MQQT_ISCONNECTED:
            print("\nNot connected to MQTT, trying to connect in 1 second")
            time.sleep(1)
            mqqt_connect("is222zf", "192.168.84.98", 1883)
        else:
            if BUTTON_PRESSED:
                # Lighting on yellow button
                Yellow_Button_On(yellowLED_b)
                # Lighting on yellow traffic light and red pedestrian light
                Traffic_Soon_Stop(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
                # Lighting on red traffic light and red pedestrian light
                All_Stop(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
                # Lighting off yellow button
                Yellow_Button_Off(yellowLED_b)
                # Lighting on red traffic light and green pedestrian light, starting fast ticks
                Pedestrian_Go(greenLED_p, redLED_p)
                # Making tick speed slower
                Pedestrian_Soon_Stop(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
                # Lighting on yellow, red traffic lights and red pedestrian light 
                Traffic_Soon_Go(greenLED_t, yellowLED_t, redLED_t, redLED_p, greenLED_p)
            # Lighting on green traffic light and red pedestrian light
            Traffic_Go(greenLED_t, yellowLED_t, redLED_t, redLED_p)
    except OSError as err:
        print("Failed: ", str(err))
        MQQT_ISCONNECTED = False
