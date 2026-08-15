# file: sketches/apps/diagnostics.py
import time

OFF = (0, 0, 0)
COLORS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
]

class Diagnostics:
    def __init__(self, pixels, led, button):
        self.pixels = pixels
        self.led = led
        self.button = button
        self.modes = [
            ("NeoPixel Sequence Test", self.diagnose_neopixels, 0.2),
            ("LED and Button Test", self.diagnose_led_button, 0.1)
        ]

    def diagnose_neopixels(self, step):
        # Cycle through colors and light up pixels one by one
        color_idx = (step // 9) % len(COLORS)
        pixel_idx = step % 9
        
        self.pixels.fill(OFF)
        self.pixels[pixel_idx] = COLORS[color_idx]
        self.pixels.show()
        
        # Toggle built-in back LED with pixel transitions
        self.led.value = (pixel_idx % 2 == 0)

    def diagnose_led_button(self, step):
        # Keep built-in LED on, except turn off if button is pressed
        is_pressed = not self.button.value
        self.led.value = not is_pressed
        
        # Draw a checkmark or indicator pattern on the NeoPixels
        # Heart/V pattern: pixels 3, 7, 5
        self.pixels.fill(OFF)
        color = (0, 255, 0) if is_pressed else (50, 50, 50)
        self.pixels[3] = color
        self.pixels[7] = color
        self.pixels[5] = color
        self.pixels.show()

# End of file: sketches/apps/diagnostics.py
