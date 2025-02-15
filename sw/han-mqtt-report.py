#!/bin/python3

import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import re
import serial
import yaml

# Map telegram to mqtt topic
topics = {
    "0-0:1.0.0": "timestamp",
    "1-0:1.8.0": "consumption",
    "1-0:2.8.0": "return_delivery",
    "1-0:3.8.0": "consumption_reactive",
    "1-0:4.8.0": "return_delivery_reactive",
    "1-0:1.7.0": "actual_consumption",
    "1-0:2.7.0": "actual_return_delivery",
    "1-0:3.7.0": "actual_consumption_reactive",
    "1-0:4.7.0": "actual_return_delivery_reactive",
    "1-0:21.7.0": "l1_instant_power_usage",
    "1-0:22.7.0": "l1_instant_power_delivery",
    "1-0:23.7.0": "l1_reactive_power_usage",
    "1-0:24.7.0": "l1_reactive_power_delivery",
    "1-0:41.7.0": "l2_instant_power_usage",
    "1-0:42.7.0": "l2_instant_power_delivery",
    "1-0:43.7.0": "l2_reactive_power_usage",
    "1-0:44.7.0": "l2_reactive_power_delivery",
    "1-0:61.7.0": "l3_instant_power_usage",
    "1-0:62.7.0": "l3_instant_power_delivery",
    "1-0:63.7.0": "l3_reactive_power_usage",
    "1-0:64.7.0": "l3_reactive_power_delivery",
    "1-0:32.7.0": "l1_voltage",
    "1-0:52.7.0": "l2_voltage",
    "1-0:72.7.0": "l3_voltage",
    "1-0:31.7.0": "l1_current",
    "1-0:51.7.0": "l2_current",
    "1-0:71.7.0": "l3_current",
}

root_topic = "sensors/power/p1meter"

def loadConfig(config_file):
    with open(config_file, 'r') as ymlfile:
        try:
            config = yaml.safe_load(ymlfile)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def main(config):
    config_yaml = loadConfig(config)

    # Initialize serial port
    try:
        ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=12)
    except:
        print('FAIL: Could not open serial port')
        exit(1)

    # Initialize the mqtt connection
    client = mqtt.Client()

    if config_yaml['mqtt']['username'] != None and config_yaml['mqtt']['password'] != None:
        client.username_pw_set(config_yaml['mqtt']['username'], config_yaml['mqtt']['password'])

    client.connect(config_yaml['mqtt']['broker'])
    client.loop_start()

    interval = int(config_yaml['mqtt']['report_interval'])

    while True:
        # Just use one telegram of out ten
        for i in range(interval):
            mvpos=0
            line = ser.readline()
            while line[0] != ord('/'):
                line = ser.readline()

        while line[0] != ord('!'):
            line = ser.readline()
            data = (re.split('\*|W|\(', str(line)[2:]))

            if len(data) > 1 and data[0] != "0-0:1.0.0":
                topic = ("{0}/{1}".format(root_topic, topics[data[0]]))
                client.publish(topic, data[1])

    ser.close()

main("/etc/han-mqtt-config.yaml")

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
