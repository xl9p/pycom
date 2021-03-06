import paho.mqtt.client as mqtt
import time
import random as rnd
import sys


def on_pb(client, userdata, result):
    pass

def send_vib(client, data):
     client.publish("is222zf/sensors/vib", data)

def send_bpm(client, data):
     client.publish("is222zf/sensors/bpm", data)

def send_gyro(client, data):
     client.publish("is222zf/sensors/gyro", data)

def send(client, vib, gyro, bpm, timestamp, deviceID):
    client.publish("is222zf/sensorsData/", ('{ "deviceID":%i, "sensors":{ "vibration":%i, "gyroscope":%i, "bpm":%i}, "timestamp":%i }') % (deviceID, vib, gyro, bpm, timestamp))

print("Sending")

client = mqtt.Client("is222zf")
client.on_publish = on_pb
client.connect("localhost", 1883, 60)

count = 0

while count < 10:
    try:
        send(client, rnd.randint(0, 25000), rnd.randint(0, 25000), rnd.randint(0, 25000), time.time(), float(sys.winver))
        time.sleep(1)
        count += 1
    except OSError as err:
        print("Failed: ", str(err))


