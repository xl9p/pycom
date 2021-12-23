import paho.mqtt.client as mqtt
import mysql.connector
import time
import json


_GYRO = None
_VIB = None
_BPM = None

_PAYLOADJSON = None

def on_msg(client, userdata, msg):
    global _PAYLOADJSON

    _PAYLOADJSON = msg.payload.decode()

def on_cnnct(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("is222zf/sensorsData/")

def checkIfExists(cursor, value, table, coulumn):
    cursor.execute("""SELECT * FROM """+ f"""{table}""" +""" WHERE """+ f"""{coulumn}""" +"""=%s""", (value,))
    cursor.fetchall()
    returnedRows = cursor.rowcount

    if returnedRows > 0:
        return True
    else:
        return False


def getConnection(Host, User, Password="", Database = "telemetry"):
    connection = mysql.connector.connect(
            host=Host,
            user=User,
            password=Password,
            database=Database
            )
    return connection


client = mqtt.Client()
client.on_message = on_msg
client.on_connect = on_cnnct
client.connect("localhost", 1883, 60)

msqlConnection = getConnection(Host="localhost", User="root", Database="telemetry")
msqlCursor = msqlConnection.cursor()

count = 0

client.loop_start()
while True: 
    try:
        if _PAYLOADJSON:

            js = json.loads(_PAYLOADJSON)
            print("\nDevice: " + str(js["deviceID"]))
            
            device = js["deviceID"]
            sensors = js["sensors"]
            timestamp = js["timestamp"]

            result = checkIfExists(msqlCursor, device, "devicesId", "name" )

            if result is True:
                pass
            else:
                msqlCursor.execute("""INSERT INTO devicesId (name) VALUES (%s)""", (device,))
                msqlConnection.commit()

            for sensor in sensors:
                result = checkIfExists(msqlCursor, sensor, "sensors", "sensorType")
                if result is True:
                    print(sensor + " exists")
                else:
                    #insert sensor
                    pass

                msqlCursor.execute("""SELECT * FROM telemetrydata INNER JOIN devicesid ON 
                                   telemetrydata.deviceID=devicesid.deviceID INNER JOIN sensors ON 
                                   telemetrydata.sensorID=sensors.sensorID WHERE sensors.sensorType=%s
                                   AND devicesid.name=%s AND telemetrydata.timestamp=%s""", (sensor, device, timestamp))
                msqlCursor.fetchall()
                returnedRows = msqlCursor.rowcount

                if returnedRows > 0:
                    print("\ntelemetry data exists")
                else:
                    print(str(sensors[sensor]))
                    msqlCursor.execute("""INSERT INTO telemetrydata (sensorID, deviceID, data, timestamp)
                                          SELECT s.sensorID, d.deviceID, %s, %s
                                          FROM sensors AS s
                                          CROSS JOIN devicesid AS d
                                          WHERE s.sensorType=%s
                                          AND d.name=%s""", (sensors[sensor], timestamp, sensor, device))
                    msqlConnection.commit()

            print("\nVibration: " + str(js["sensors"]["vibration"]))
            print("Gyroscope: " + str(js["sensors"]["gyroscope"]))
            print("BPM: " + str(js["sensors"]["bpm"]))
            print("Time: " + str(time.ctime(js["timestamp"])))
            _PAYLOADJSON = None
        
    except Exception as err:
        if isinstance(err, KeyboardInterrupt):
            client.loop_stop()
        print(str(err))