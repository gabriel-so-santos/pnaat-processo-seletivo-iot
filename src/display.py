

class Display:
    def __init__(self, oled):
        self.oled = oled

    def update(self, temp, hum, temp_trend, hum_trend, temp_limit):
        self.oled.fill(0)

        self.oled.text(f"T:{temp:.1f}C", 0, 0)
        self.oled.text(f"H:{hum:.1f}%", 0, 16)

        self.oled.text(f"d:{temp_trend}", 64, 0)
        self.oled.text(f"d:{hum_trend}", 64, 16)

        self.oled.text(f"lim:{temp_limit:.1f}C", 0, 54)

        self.oled.show()