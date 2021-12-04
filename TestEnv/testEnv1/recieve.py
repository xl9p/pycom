import paho.mqtt.client as mqtt
import time


_ISSENDING = None
_TRAFFIC = None
_PEDESTRIAN = None

def on_msg(client, userdata, msg):
    global _ISSENDING
    global _TRAFFIC
    global _PEDESTRIAN

    if "issending" in msg.topic:
        _ISSENDING = str(msg.payload.decode())
    if "traffic" in msg.topic:
        _TRAFFIC = str(msg.payload.decode())
    if "pedestrian" in msg.topic:
        _PEDESTRIAN = str(msg.payload.decode())

def on_cnnct(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("is222zf/feeds/lights/#")


def mainloop():
    global _ISSENDING
    global _TRAFFIC
    global _PEDESTRIAN

    client = mqtt.Client()
    client.on_message = on_msg
    client.on_connect = on_cnnct
    client.connect("localhost", 1883, 60)

    client.loop_start()

    while True: 
        try:
            if _ISSENDING == None:
                pass
            elif "1" in _ISSENDING:
                time.sleep(0.2)
                print("\nTraffic: " + _TRAFFIC)
                print("Pedestrian: " + _PEDESTRIAN)
        except Exception as err:
            print(str(err))
    #client.loop_stop()

mainloop()