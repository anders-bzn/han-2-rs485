# han-2-rs485
A small board that converts signal level from the HAN-port on swedish electricity power meter to RS-485. There is no connection for ground so a galvanically separated receiver is recommended. The board fits into a small ELKO standard connection box.

Created with KiCad 7.0 and [kicad-jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools) plugin for creating fabrication files.

This is used together with a Raspberry Pi with a RS-485 HAT

## Software
Small python program for publishing MQTT data. It has one script that sets up the RPi and installs a service. The p1_sensors.yaml is a template for mapping sensors into Home Assistant. The content should be pasted into configuration.yaml in Home Assistant.

### Prerequisites

1. Has a local MQTT (tested with mosquitto) server without authentication
2. Has paho mqtt module installed

## Acknowledgement
Acknowledgement to this github project: https://github.com/UdoK/esp8266_p1meter_sv from which I copied the mqtt topics.