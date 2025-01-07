#!/bin/bash

CFILE="/boot/firmware/config.txt"

# Overlay for serial port
if [ -z "$(grep -x "dtoverlay=miniuart-bt" "$CFILE")" ]; then
    echo "dtoverlay=miniuart-bt" >> "$CFILE"
    echo Add "dtoverlay=miniuart-bt" to "$CFILE"
fi

if [ -z "$(grep -x "enable_uart=1" "$CFILE")" ]; then
    echo "enable_uart=1" >> "$CFILE"
    echo Add "enable_uart=1" to "$CFILE"
fi

cp han-mqtt-report.py /usr/bin
cp han-mqtt.service /etc/systemd/system
systemctl enable han-mqtt.service
