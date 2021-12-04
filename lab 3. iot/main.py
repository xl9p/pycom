from mqtt import MQTTClient_lib
import machine
import time
from network import WLAN


def sub_cb(topic, msg):
   print(msg)

print("lab 3")

wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid="Galaxy S96a30", auth=(WLAN.WPA2, "smwm7221"))

while not wlan.isconnected():
   machine.idle()

print("connected")

client = MQTTClient_lib("is222zf", "192.168.190.98", port=1883)
client.set_callback(sub_cb)
client.connect()
print("MQTT connected")

client.subscribe(topic="is222zf/feeds/light")
# client.subscribe(topic="is222zf/feeds/humidity")
print("subscribed")


while True:
   print("Sending ON")
   client.publish(topic="is222zf/feeds/light", msg="ON")
   client.check_msg()
   time.sleep(1)
   print("Sending OFF")
   client.publish(topic="is222zf/feeds/light", msg="OFF")
   client.check_msg()
   time.sleep(1)