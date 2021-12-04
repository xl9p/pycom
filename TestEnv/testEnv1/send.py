import paho.mqtt.client as mqtt
import time


COUNT = 1
MQQT_ISCONNECTED = False
BUTTON_PRESSED = False

def Traffic_Go():
    global COUNT
    print("Traffic: Green")
    print("Pedestrian: Red")
    
    if COUNT == 1:
        client.publish("is222zf/feeds/lights/issending/", "1")
        time.sleep(0.2)
        client.publish("is222zf/feeds/lights/traffic/", "GREEN")
    
        client.publish("is222zf/feeds/lights/pedestrian/", "RED")

        client.publish("is222zf/feeds/lights/issending/", "0")
    COUNT += 1

def Pedestrian_Go():
    print("\nTraffic is not allowed to go, you can cross the road.")
    print("Traffic: red")
    print("Pedestrian: green")
    print("Fast ticks")

    client.publish("is222zf/feeds/lights/issending/", "1")
    time.sleep(0.2)
    client.publish("is222zf/feeds/lights/traffic/", "RED")

    client.publish("is222zf/feeds/lights/pedestrian/", "GREEN")

    client.publish("is222zf/feeds/lights/issending/", "0")
    time.sleep(2.8)
    
def All_Stop():
    print("\nNo one is allowed to cross.")
    print("Traffic: red")
    print("Pedestrian: red")

    client.publish("is222zf/feeds/lights/issending/", "1")
    time.sleep(0.2)
    client.publish("is222zf/feeds/lights/traffic/", "RED")

    client.publish("is222zf/feeds/lights/pedestrian/", "RED")
    
    client.publish("is222zf/feeds/lights/issending/", "0")
    time.sleep(0.8)

def Traffic_Soon_Stop():
    print("\nTraffic soon will be stopped.")
    print("Traffic: yellow")
    print("Pedestrian: red")

    client.publish("is222zf/feeds/lights/issending/", "1")
    time.sleep(0.2)
    client.publish("is222zf/feeds/lights/traffic/", "YELLOW")
    client.publish("is222zf/feeds/lights/pedestrian/", "RED")

    client.publish("is222zf/feeds/lights/issending/", "0")
    time.sleep(1.8)

def Traffic_Soon_Go():
    global COUNT

    print("\nTraffic will be allowed to go soon, do not cross the road.")
    print("Traffic: yellow, red")
    print("Pedestrian: red")

    client.publish("is222zf/feeds/lights/issending/", "1")
    time.sleep(0.2)
    client.publish("is222zf/feeds/lights/traffic/", "YELLOW, RED")

    client.publish("is222zf/feeds/lights/pedestrian/", "RED")

    client.publish("is222zf/feeds/lights/issending/", "0")
    time.sleep(0.8)

    COUNT = 1

def Pedestrian_Soon_Stop():
    print("\nTraffic will be allowed to go soon, finish crossing the road.")
    print("Traffic: red")
    print("Pedestrian: green")
    print("Slow ticks")

    client.publish("is222zf/feeds/lights/issending/", "1")
    time.sleep(0.2)
    client.publish("is222zf/feeds/lights/traffic/", "RED")

    client.publish("is222zf/feeds/lights/pedestrian/", "GREEN")

    client.publish("is222zf/feeds/lights/issending/", "0")
    time.sleep(0.8)

def on_pb(client, userdata, result):
    pass

print("Lab 3. Traffic lights, sending")


client = mqtt.Client("is222zf")
client.on_publish = on_pb
client.connect("localhost", 1883, 60)


while True:
    try:
        # Lighting on yellow traffic light and red pedestrian light
        Traffic_Soon_Stop()
        # Lighting on red traffic light and red pedestrian light
        All_Stop()
        # Lighting on red traffic light and green pedestrian light, starting fast ticks
        Pedestrian_Go()
        # Making tick speed slower
        Pedestrian_Soon_Stop()
        # Lighting on yellow, red traffic lights and red pedestrian light 
        Traffic_Soon_Go()
        # Lighting on green traffic light and red pedestrian light
        Traffic_Go()
        time.sleep(10)
    except OSError as err:
        print("Failed: ", str(err))


