from mqtt import MQTTClient_lib
import machine
import time
from network import WLAN


MQQT_ISCONNECTED = False
_ISSENDING = "0"
_TRAFFIC = None
_PEDESTRIAN = None
CLIENT = None

def sub_cb(topic, msg):
    global _ISSENDING
    global _PEDESTRIAN
    global _TRAFFIC

    if "issending" in topic:
        _ISSENDING = str(msg.decode())
    if "traffic" in topic:
        _TRAFFIC = str(msg.decode())
    if "pedestrian" in topic:
        _PEDESTRIAN = str(msg.decode())

def wlan_connect(name, passw, wlan_obj):
    wlan_obj.connect(ssid=str(name), auth=(WLAN.WPA2, str(passw))) #smwm7221

    while not wlan_obj.isconnected():
        machine.idle()

    print("connected")
    return wlan_obj

def mqqt_cnct_and_sub(device, ipaddr, port):
    global MQQT_ISCONNECTED
    global CLIENT

    CLIENT = MQTTClient_lib(str(device), str(ipaddr), port=int(port))
    CLIENT.set_callback(sub_cb)
    CLIENT.connect()

    CLIENT.subscribe(topic="is222zf/feeds/lights/issending/")
    CLIENT.subscribe(topic="is222zf/feeds/lights/traffic/")
    CLIENT.subscribe(topic="is222zf/feeds/lights/pedestrian/")

    MQQT_ISCONNECTED = True
    print("MQTT connected")


wlan = WLAN(mode=WLAN.STA)

while True:
    try:
        if not wlan.isconnected():
            print("Not connected to WLAN, trying to connect in 1 second")
            time.sleep(1)
            wlan = wlan_connect("Galaxy S96a30", "smwm7221", wlan)
        if not MQQT_ISCONNECTED:
            print("Not connected to MQTT, trying to connect in 1 second")
            time.sleep(1)
            mqqt_cnct_and_sub("is222zf_reader", "192.168.123.225", 1883)

        if "1" in _ISSENDING:
            print("\nReading data")
            time.sleep(0.2)
            while _TRAFFIC == None:
                CLIENT.check_msg()
            while _PEDESTRIAN == None:
                CLIENT.check_msg()
            print("Traffic: " + str(_TRAFFIC))
            print("Pedestrian: " + str(_PEDESTRIAN))
            _ISSENDING = None
            _TRAFFIC = None
            _PEDESTRIAN = None
        CLIENT.check_msg()

    except OSError as err:
        print(str(err))
        MQQT_ISCONNECTED = False
    