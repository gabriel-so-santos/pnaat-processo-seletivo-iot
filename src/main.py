from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from circular_buffer import CircularBuffer
import dht
import time

import random as rd

print("Teste")

OLED_WIDTH: int = 128
OLED_HEIGHT: int = 64
READ_INTERVAL: int = 250  # measured in ms

MAX_HISTORY_SIZE: int = 16

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

pot_adc = ADC(Pin(35))
pot_adc.atten(ADC.ATTN_11DB)

dht22 = dht.DHT22(Pin(13))

led = Pin(12, Pin.OUT)

pot_value: int = 0
t_limit: float = 0.0

temperature: float = 0.0
humidity: float = 0.0

t_diff: float = 0.0
h_diff: float = 0.0
t_prev_diff: float = 0.0
h_prev_diff: float = 0.0

history = CircularBuffer(size=MAX_HISTORY_SIZE)

last_update = time.ticks_ms()
time_now = time.ticks_ms()


def get_trend(curr_diff: float, prev_diff: float, epsilon: float = 0.05) -> str:
    """
    Returns a formatted trend string (trend_char + diff):

    + : increasing
    - : decreasing
    = : stable
    ~ : oscillation (change in direction)

    epsilon defines the threshold for 'stable'
    """

    # Determine current direction
    if abs(curr_diff) < epsilon:
        trend_char = '='
    elif curr_diff > 0:
        trend_char = '+'
    else:
        trend_char = '-'

    # Detect oscillation (sign change, ignoring near-zero noise)
    if (
            abs(prev_diff) >= epsilon and
            abs(curr_diff) >= epsilon and
            (curr_diff * prev_diff < 0)
    ):
        trend_char = '~'

    return f"{trend_char}{abs(curr_diff):.1f}"


while True:

    time_now = time.ticks_ms()

    if time.ticks_diff(time_now, last_update) >= READ_INTERVAL:
        last_update = time_now

        dht22.measure()
        temperature = dht22.temperature()  # reads within range -40°C .. 80°C
        humidity = dht22.humidity()        # reads within range    0% .. 100%
        pot_value = pot_adc.read()         # reads within range  0000 .. 4095

        # DEBUG
        # temperature = rd.uniform(-40.0, 80.0)
        # humidity = rd.uniform(0.0, 100.0)

        t_limit = pot_value * 120 / 4096 - 40

        if temperature >= t_limit:
            led.value(1)
        else:
            led.value(0)

        last_insertion: tuple[float, float] = history.last()
        history.push((temperature, humidity))

        if last_insertion is None:
            t_diff = 0
            h_diff = 0
        else:
            prev_temp, prev_hum = last_insertion
            t_diff = temperature - prev_temp
            h_diff = humidity - prev_hum

        t_trend: str = get_trend(t_diff, t_prev_diff)
        h_trend: str = get_trend(h_diff, h_prev_diff)

        t_prev_diff = t_diff
        h_prev_diff = h_diff

        oled.fill(0)

        oled.text(f"T:{temperature:.1f}C", 0, 0)
        oled.text(f"H:{humidity:.1f}%", 0, 16)

        oled.text(f"d:{t_trend}", 64, 0)
        oled.text(f"d:{h_trend}", 64, 16)

        oled.text(f"lim:{t_limit:.1f}C", 0, 54)

        oled.show()