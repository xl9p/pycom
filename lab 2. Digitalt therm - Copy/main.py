from network import LoRa
import socket
import time
import ubinascii
import ustruct
import time
from machine import Pin
from dth import DTH


def encode_float(temp):
    packet = ustruct.pack('f', temp)

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

    s.setblocking(True)

    s.send(packet)

    s.setblocking(False)
    
    data = s.recv(64)
    print(data)
    print("Unpacked value is:", ustruct.unpack('f', packet)[0])
    print("data sent")

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('40E004E1CD3531F4DEC22622E110CF1B')
dev_eui = ubinascii.unhexlify('70B3D57ED0049D35')

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')

th = DTH('P11', 0)

while True:
    print("\nDigital sensor's data:")
    result = th.read()
    if result.is_valid():
        temp = float(result.temperature)
        humid = float(result.humidity)
        print("Results are valid.")
        print("Temperature: " + str(temp)+"C")
        print("Humidity: " + str(humid)+"%")
        encode_float(temp)

    time.sleep(65)