from time import sleep
import os
import binascii
from Crypto.Cipher import AES
from adafruit_ble import BLERadio
from adafruit_ble.services.gmsservice import GMS
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

def decryption(ciphertext):
    key = (b"1111222233334444")
    serial_number = binascii.unhexlify(ciphertext)
    decryptor = AES.new(key, AES.MODE_ECB)
    plaintext = decryptor.decrypt(serial_number)
    print(plaintext.decode("utf-8"))

ble = BLERadio()
found = set()

# Scan and detect dongles
for advertisement in ble.start_scan(Advertisement, timeout=10):
    device_name = advertisement.complete_name
 
    if device_name and device_name not in found:
        if device_name.startswith("ble_device"):
            # Add dongle to found list 
            found.add(device_name)
            # Establish connection with dongle
            GMS_connection = ble.connect(advertisement)
            print("Connected to " + device_name)
            # Tranmission with dongle
            if GMS_connection and GMS_connection.connected:
                GMS_transmission = GMS_connection[GMS]
                GMS_transmission.write(b"Authentication")
                ble_serial_number = GMS_transmission.read(32).decode("utf-8")
                print(ble_serial_number)
                decryption(ble_serial_number)
#                if ble_serial_number:
 #                   print(ble_serial_number)
  #              public_key = GMS_transmission.read(64).decode("utf-8")
   #             if public_key:
    #                print(public_key)
                GMS_connection.disconnect()
                
ble.stop_scan()            

#s.encode("utf-8")