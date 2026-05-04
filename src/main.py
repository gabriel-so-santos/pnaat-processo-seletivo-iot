#import random
import time

import dht
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C

import analysis
from circular_buffer import CircularBuffer
from display import Display


print("Teste") # required by CI

OLED_WIDTH: int = 128
OLED_HEIGHT: int = 64
READ_INTERVAL: int = 250  # measured in ms
MAX_HISTORY_SIZE: int = 16

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
display = Display(oled)

pot_adc = ADC(Pin(35))
pot_adc.atten(ADC.ATTN_11DB)

dht22 = dht.DHT22(Pin(13))

led = Pin(12, Pin.OUT)

pot_value: int = 0
temp_limit: float = 0.0

temperature: float = 0.0
humidity: float = 0.0

temp_diff: float = 0.0
hum_diff: float = 0.0
temp_prev_diff: float = 0.0
hum_prev_diff: float = 0.0

history = CircularBuffer(size=MAX_HISTORY_SIZE)

last_update = time.ticks_ms()
time_now = time.ticks_ms()

# ---------- Main Loop ----------

while True:
    time_now = time.ticks_ms()

    if time.ticks_diff(time_now, last_update) >= READ_INTERVAL:
        last_update = time_now

        dht22.measure()
        temperature = dht22.temperature()  # reads within range -40°C .. 80°C
        humidity = dht22.humidity()        # reads within range    0% .. 100%
        pot_value = pot_adc.read()         # reads within range  0000 .. 4095

        # ---------- Debug ----------
        # temperature = random.uniform(-40.0, 80.0)
        # humidity = random.uniform(0.0, 100.0)
        # ---------------------------

        temp_limit = pot_value * 120 / 4096 - 40

        if temperature >= temp_limit:
            led.value(1)
        else:
            led.value(0)

        last_insertion: tuple[float, float] = history.last()
        history.push((temperature, humidity))

        if last_insertion is None:
            temp_diff = 0
            hum_diff = 0
        else:
            prev_temp, prev_hum = last_insertion
            temp_diff = temperature - prev_temp
            hum_diff = humidity - prev_hum

        temp_trend: str = analysis.get_trend(temp_diff, temp_prev_diff)
        hum_trend: str = analysis.get_trend(hum_diff, hum_prev_diff)

        temp_prev_diff = temp_diff
        hum_prev_diff = hum_diff

        display.update(
            temperature, humidity,
            temp_trend, hum_trend,
            temp_limit)