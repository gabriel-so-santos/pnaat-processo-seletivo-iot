class Display:
    """
    Handles OLED rendering for sensor data visualization.
    """

    def __init__(self, oled):
        """
        Initialize display with SSD1306 OLED instance.

        Args:
            oled: SSD1306 OLED display driver instance.
        """
        self.oled = oled

    def update(self, temp: float, hum: float, temp_trend: str, hum_trend: str, temp_limit: float):
        """
        Render sensor values and trends on the OLED screen.

        Args:
            temp (float): Current temperature value.
            hum (float): Current humidity value.
            temp_trend (str): Temperature trend indicator.
            hum_trend (str): Humidity trend indicator.
            temp_limit (float): Current temperature threshold
        """
        self.oled.fill(0)

        self.oled.text(f"T:{temp:.1f}C", 0, 0)
        self.oled.text(f"H:{hum:.1f}%", 0, 16)

        self.oled.text(f"d:{temp_trend}", 64, 0)
        self.oled.text(f"d:{hum_trend}", 64, 16)

        self.oled.text(f"lim:{temp_limit:.1f}C", 0, 54)

        self.oled.show()