#!/usr/bin/env python3
"""Raspberry Pi GPIO 控制範例"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
LED_PIN = 11
BUTTON_PIN = 12

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def blink_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(1)

def button_led():
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

def demo():
    print("=" * 60)
    print("Raspberry Pi GPIO Demo")
    print("=" * 60)

    print("\n--- LED Blink ---")
    print("Blinking LED 3 times...")
    for _ in range(3):
        blink_led()

    print("\n--- Button LED Control ---")
    print("Press Ctrl+C to exit")
    try:
        while True:
            button_led()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")

    GPIO.cleanup()
    print("Done!")

if __name__ == "__main__":
    demo()