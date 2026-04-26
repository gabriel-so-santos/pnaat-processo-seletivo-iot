from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import dht
import time

OLED_WIDTH:  int = 128
OLED_HEIGHT: int = 64

MAX_HISTORY_SIZE: int = 16

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

pot_adc = ADC(Pin(35))
pot_adc.atten(ADC.ATTN_11DB)

dht22 = dht.DHT22(Pin(13))

led = Pin(12, Pin.OUT)

pot_value:   int   = 0
t_limit:     float = 0.0

temperature: float = 0.0
humidity:    float = 0.0

t_diff:      float = 0.0
h_diff:      float = 0.0

t_history:   list  = []
h_history:   list  = []

print("Teste")

ITERATIONS = 10
for _ in range(ITERATIONS):

    dht22.measure()
    temperature = dht22.temperature() # reads within range -40°C - 80°C
    humidity    = dht22.humidity()    # reads within range 0% - 100%
    pot_value   = pot_adc.read()      # reads within range 0000 - 4095

    t_limit = pot_value * 120 / 4096 - 40

    if temperature >= t_limit:
        led.value(1)
    else:
        led.value(0)

    if len(t_history) >= MAX_HISTORY_SIZE:
        t_history.pop(0)
        h_history.pop(0)

    if len(t_history) == 0:
        t_diff = 0
        h_diff = 0
    else:
        t_diff = temperature - t_history[-1]
        h_diff = humidity    - h_history[-1]

    t_history.append(temperature)
    h_history.append(humidity)

    temperature = round(temperature, 2)
    humidity    = round(humidity, 2)
    t_diff      = round(t_diff, 2)
    h_diff      = round(h_diff, 2)
    t_limit     = round(t_limit, 2)

    oled.fill(0)

    oled.text("T:" + str(temperature) + "C", 0, 0)
    oled.text("H:" + str(humidity)    + "%", 0, 16)

    oled.text("(" + str(t_diff) + ")", 64, 0)
    oled.text("(" + str(h_diff) + ")", 64, 16)

    oled.text("lim:" + str(t_limit)  + "C", 0, 54)

    oled.show()

    time.sleep(0.5)