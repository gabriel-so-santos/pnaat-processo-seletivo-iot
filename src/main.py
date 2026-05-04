"""
Main entry point for the ESP32 IoT environmental monitoring system.

This module orchestrates sensor acquisition, signal processing,
trend analysis, and OLED display updates.

Features:
- Temperature and humidity monitoring via DHT22
- Dynamic temperature threshold via potentiometer (ADC)
- Circular buffer for historical data
- Trend analysis (+, -, =, ~)
- OLED real-time visualization
- LED alert when threshold is exceeded
"""

import random
import time

# CI time limitation
START_TIME = time.ticks_ms()
MAX_RUNTIME = 9_000  # 9 seconds
print("Teste") # required by CI

import dht
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C

import analysis
from circular_buffer import CircularBuffer
from display import Display


# ------------ Configuration Constants -------------
OLED_WIDTH = 128
OLED_HEIGHT = 64
READ_INTERVAL = 500  # measured in ms
MAX_HISTORY_SIZE = 16

# ------------ Hardware Initialization -------------
# I2C + OLED display
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
display = Display(oled)

# ADC (potentiometer for dynamic threshold)
pot_adc = ADC(Pin(35))
pot_adc.atten(ADC.ATTN_11DB)

# DHT22 sensor (temperature + humidity)
dht22 = dht.DHT22(Pin(13))

# LED actuator (alert indicator)
led = Pin(12, Pin.OUT)

# ------------ Runtime State Variables -------------
temperature = 0.0
humidity = 0.0

temp_diff = 0.0
hum_diff = 0.0

temp_prev_diff = 0.0
hum_prev_diff = 0.0

temp_limit = 0.0
pot_value = 0

# Circular buffer for history-tracking sensor data
history = CircularBuffer(size=MAX_HISTORY_SIZE)

# Timing control
last_update = time.ticks_ms()
time_now = time.ticks_ms()


# ------------------- Main Loop --------------------
while True:
    time_now = time.ticks_ms()

    # break before reach max runtime
    if time.ticks_diff(time_now, START_TIME) >= MAX_RUNTIME:
        break

    if time.ticks_diff(time_now, last_update) >= READ_INTERVAL:
        last_update = time_now

        # --------------- Data Acquisition -----------------
        dht22.measure()
        temperature = dht22.temperature()  # reads within range -40°C .. 80°C
        humidity = dht22.humidity()        # reads within range    0% .. 100%
        pot_value = pot_adc.read()         # reads within range  0000 .. 4095

        # Map potentiometer read to temperature range
        temp_limit = pot_value * 120 / 4096 - 40

        # Debug
        # temperature = random.uniform(-40.0, 80.0)
        # humidity = random.uniform(0.0, 100.0)

        # ------------------- LED Alert --------------------
        if temperature >= temp_limit:
            led.value(1)
        else:
            led.value(0)

        # --------------- History Tracking -----------------
        last_insertion: tuple[float, float] = history.last()
        history.push((temperature, humidity))

        if last_insertion is None:
            temp_diff = 0
            hum_diff = 0
        else:
            prev_temp, prev_hum = last_insertion
            temp_diff = temperature - prev_temp
            hum_diff = humidity - prev_hum

        # ---------------- Trend Analysis ------------------
        temp_trend: str = analysis.get_trend(temp_diff, temp_prev_diff)
        hum_trend: str = analysis.get_trend(hum_diff, hum_prev_diff)

        temp_prev_diff = temp_diff
        hum_prev_diff = hum_diff

        # -------------------- Display ---------------------
        display.update(
            temperature, humidity,
            temp_trend, hum_trend,
            temp_limit)