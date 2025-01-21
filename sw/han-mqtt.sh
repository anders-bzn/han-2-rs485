#!/bin/bash

# Must be root to install things
if [ $USER != "root" ]; then
    echo User must be root
    exit 1
fi

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

# Python dependencies
apt -y install python3-yaml
apt -y install python3-paho-mqtt

# Copy config, change if needed
cp han-mqtt-config.yaml /etc/

# Install service
cp han-mqtt-report.py /usr/bin
cp han-mqtt.service /etc/systemd/system
systemctl enable han-mqtt.service
