# Run this script to find which ports are available on your computer
# This is for HowManyFingers.py

import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(port.device)
