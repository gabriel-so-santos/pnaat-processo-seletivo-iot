from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from circular_buffer import CircularBuffer
import dht
import time

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

history = CircularBuffer(size=MAX_HISTORY_SIZE)

last_update = time.ticks_ms()
time_now = time.ticks_ms()

while True:
    time_now = time.ticks_ms()

    if time.ticks_diff(time_now, last_update) >= READ_INTERVAL:
        last_update = time_now

        dht22.measure()
        temperature = dht22.temperature()  # reads within range -40°C .. 80°C
        humidity = dht22.humidity()        # reads within range    0% .. 100%
        pot_value = pot_adc.read()         # reads within range  0000 .. 4095

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
            t_diff = temperature - last_insertion[0]
            h_diff = humidity - last_insertion[1]

        oled.fill(0)

        oled.text(f"T:{temperature:.1f}C", 0, 0)
        oled.text(f"H:{humidity:.1f}%", 0, 16)

        oled.text(f"d:{t_diff:.1f}", 64, 0)
        oled.text(f"d:{h_diff:.1f}", 64, 16)

        oled.text(f"lim:{t_limit:.1f}C", 0, 54)

        oled.show()