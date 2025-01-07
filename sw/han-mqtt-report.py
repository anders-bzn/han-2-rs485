#!/bin/python3
import serial
import paho.mqtt.publish as publish


workbuffert = bytearray(1024)
mv = memoryview(workbuffert)

try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=12)
except:
    print('FAIL: Could not open serial port')
    exit(1)

while True:
    for i in range(15):
        mvpos=0
        line = ser.readline()
        while line[0] != ord('/'):
            line = ser.readline()

        mv[mvpos : mvpos+len(line)] = line
        mvpos += len(line)

        while line[0] != ord('!'):
            line = ser.readline()
            mv[mvpos : mvpos+len(line)] = line
            mvpos += len(line)
        #    print(line)

        #print ('END', line[1:])
    #print ("Publish")
    publish.single("sensor/power/house", mv.tobytes(), qos=0, retain=False, hostname="localhost",
                    port=1883, client_id="power-collect", keepalive=60, will=None, auth=None,
                    tls=None)
ser.close()
