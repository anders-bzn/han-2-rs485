#!/bin/python3
import re
import serial
import paho.mqtt.publish as publish

# Map telegram to mqtt topica
topics = {
    "0-0:1.0.0": "timestamp",
    "1-0:1.8.0": "consumption",
    "1-0:2.8.0": "returndelivery",
    "1-0:3.8.0": "consumption_reactive",
    "1-0:4.8.0": "returndelivery_reactive",
    "1-0:1.7.0": "actual_consumption",
    "1-0:2.7.0": "actual_returndelivery",
    "1-0:3.7.0": "actual_consumption_reactive",
    "1-0:4.7.0": "actual_returndelivery_reactive",
    "1-0:21.7.0": "l1_instant_power_usage",
    "1-0:41.7.0": "l1_instant_power_delivery",
    "1-0:61.7.0": "l2_instant_power_usage",
    "1-0:22.7.0": "l2_instant_power_delivery",
    "1-0:42.7.0": "l3_instant_power_usage",
    "1-0:62.7.0": "l3_instant_power_delivery",
    "1-0:23.7.0": "l1_reactive_power_usage",
    "1-0:43.7.0": "l1_reactive_power_delivery",
    "1-0:63.7.0": "l2_reactive_power_usage",
    "1-0:24.7.0": "l2_reactive_power_delivery",
    "1-0:44.7.0": "l3_reactive_power_usage",
    "1-0:64.7.0": "l3_reactive_power_delivery",
    "1-0:32.7.0": "l1_voltage",
    "1-0:52.7.0": "l2_voltage",
    "1-0:72.7.0": "l3_voltage",
    "1-0:31.7.0": "l1_instant_power_current",
    "1-0:51.7.0": "l2_instant_power_current",
    "1-0:71.7.0": "l3_instant_power_current",
}

root_topic = "sensors/power/p1meter"

def postTopic(topic, value):
    publish.single(topic, value, qos=0, retain=False, hostname="localhost",
                    port=1883, client_id="power-collect", keepalive=60, will=None, auth=None,
                    tls=None)


try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=12)
except:
    print('FAIL: Could not open serial port')
    exit(1)

while True:
    # Just use one telegram of out ten
    for i in range(10):
        mvpos=0
        line = ser.readline()
        while line[0] != ord('/'):
            line = ser.readline()

    while line[0] != ord('!'):
        line = ser.readline()
        data = (re.split('\*|W|\(', str(line)[2:]))

        if len(data) > 1 and data[0] != "0-0:1.0.0":
            postTopic("{0}/{1}".format(root_topic, topics[data[0]]) ,data[1])

ser.close()

""" This is a telegram example
'0-0:1.0.0(250107213151W)\r\n'
'1-0:1.8.0(00006156.203*kWh)\r\n'
'1-0:2.8.0(00009012.076*kWh)\r\n'
'1-0:3.8.0(00000003.237*kvarh)\r\n'
'1-0:4.8.0(00003778.093*kvarh)\r\n'
'1-0:1.7.0(0001.999*kW)\r\n'
'1-0:2.7.0(0000.000*kW)\r\n'
'1-0:3.7.0(0000.000*kvar)\r\n'
'1-0:4.7.0(0000.623*kvar)\r\n'
'1-0:21.7.0(0000.279*kW)\r\n'
'1-0:41.7.0(0000.807*kW)\r\n'
'1-0:61.7.0(0000.912*kW)\r\n'
'1-0:22.7.0(0000.000*kW)\r\n'
'1-0:42.7.0(0000.000*kW)\r\n'
'1-0:62.7.0(0000.000*kW)\r\n'
'1-0:23.7.0(0000.000*kvar)\r\n'
'1-0:43.7.0(0000.000*kvar)\r\n'
'1-0:63.7.0(0000.000*kvar)\r\n'
'1-0:24.7.0(0000.357*kvar)\r\n'
'1-0:44.7.0(0000.165*kvar)\r\n'
'1-0:64.7.0(0000.100*kvar)\r\n'
'1-0:32.7.0(235.2*V)\r\n'
'1-0:52.7.0(235.9*V)\r\n'
'1-0:72.7.0(237.0*V)\r\n'
'1-0:31.7.0(002.0*A)\r\n'
'1-0:51.7.0(003.6*A)\r\n'
'1-0:71.7.0(003.9*A)\r\n'
"""