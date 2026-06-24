#!/usr/bin/env python3
"""I2C 感測器讀取範例"""

import smbus2
import time

bus = smbus2.SMBus(1)

I2C_ADDRESS = 0x77

def read_bmp180_temp():
    bus.write_byte_data(I2C_ADDRESS, 0xF4, 0x2E)
    time.sleep(0.005)
    data = bus.read_word_data(I2C_ADDRESS, 0xF6)
    return data

def scan_i2c():
    print("Scanning I2C devices...")
    devices = []
    for addr in range(0x03, 0x78):
        try:
            bus.read_byte(addr)
            devices.append(f"0x{addr:02X}")
        except:
            pass
    return devices

def demo():
    print("=" * 60)
    print("I2C Sensor Demo")
    print("=" * 60)

    print("\n--- I2C Scan ---")
    devices = scan_i2c()
    if devices:
        print(f"Found {len(devices)} devices: {devices}")
    else:
        print("No I2C devices found")

    print("\n--- BMP180 Read ---")
    for i in range(5):
        try:
            raw = read_bmp180_temp()
            print(f"Raw value: {raw}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

    print("\nDone!")

if __name__ == "__main__":
    demo()