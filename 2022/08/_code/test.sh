#!/bin/bash
set -x
cd "$(dirname "$0")" && python3 distributed_training.py
