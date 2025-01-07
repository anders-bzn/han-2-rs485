# han-2-rs458
A small board that converts signal level from the HAN-port on swedish electricity power meter to RS-485. There is no connection for ground so a galvanically separated receiver is recommended. The board fits into a small ELKO standard connection box.

Created with KiCad 7.0 and [kicad-jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools) plugin for creating fabrication files.

## Software
Small python program for publishing MQTT data. It has one script that sets up the RPi and installs a service.

prerequisites

1. Has a local MQTT (tested with mosquitto) server without authentication
2. Has paho mqtt module installed