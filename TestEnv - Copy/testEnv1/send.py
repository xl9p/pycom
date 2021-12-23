import paho.mqtt.client as mqtt
import time
import random as rnd


def on_pb(client, userdata, result):
    pass

def send_vib(client, data):
     client.publish("is222zf/sensors/vib", data)

def send_bpm(client, data):
     client.publish("is222zf/sensors/bpm", data)

def send_gyro(client, data):
     client.publish("is222zf/sensors/gyro", data)

print("Sending")

client = mqtt.Client("is222zf")
client.on_publish = on_pb
client.connect("localhost", 1883, 60)


while True:
    try:
        send_bpm(client, 15)
        send_vib(client, 13)
        send_gyro(client, 12)
        time.sleep(1)
    except OSError as err:
        print("Failed: ", str(err))


