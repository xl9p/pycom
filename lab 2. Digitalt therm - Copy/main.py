import time
from dth import DTH
from network import LoRa
import ubinascii
import socket




app_eui = ubinascii.unhexlify('70B3D549779D7B99')
app_key = ubinascii.unhexlify('99DD8A6AE643C8A591A709672FE35C85')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
th = DTH('P11', 0)

while True:
    try:
        if not lora.has_joined():
            
        else:
            print("\nDigital sensor's data:")
            result = th.read()
            if result.is_valid():
                s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
                s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
                s.setblocking(True)
                s.send(bytes([0x01, 0x02, 0x03]))
                s.setblocking(False)
                data = s.recv(64)
                print(data)

                print("Results are valid.")
                print("Temperature: " + str(result.temperature)+"C")
                print("Humidity: " + str(result.humidity)+"%")
            else:
                print("Results may be not valid.")
                print("Temperature: " + str(result.temperature)+"C")
                print("Humidity: " + str(result.humidity)+"%")
    except Exception as err:
        print(str(err))
    time.sleep(3)

#end device id eui-70b3d57ed0049a63
# joineui 0000000000000000
#DEVeui 70B3D57ED0049A63
#App key 8F74330E23A64634D5F7F07F1234006B




# set the LoRaWAN data rate


# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)


# send some data
