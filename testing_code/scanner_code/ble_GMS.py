# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Used with ble_uart_echo_test.py. Transmits "echo" to the UARTService and receives it back.
"""

import time

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.gmsservice import GMS

ble = BLERadio()
while True:
    while ble.connected and any(
        GMS in connection for connection in ble.connections
    ):
        for connection in ble.connections:
            if GMS not in connection:
                continue
            print("echo")
            uart = connection[GMS]
            uart.write(b"echo")
            # Returns b'' if nothing was read.
            one_byte = uart.read(4)
            if one_byte:
                print(one_byte)
            print()
        time.sleep(1)

    print("disconnected, scanning")
    for advertisement in ble.start_scan(ProvideServicesAdvertisement, timeout=1):
        if GMS not in advertisement.services:
            continue
        ble.connect(advertisement)
        print("connected")
        break
    ble.stop_scan()
