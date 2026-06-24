#!/usr/bin/env bash
set -x
cd /Users/Shared/ccc/magazine/aiprogrammer/2015/11/_code/raspberry_pi
python3 gpio_example.py
python3 i2c_sensor.py
python3 mqtt_client.py