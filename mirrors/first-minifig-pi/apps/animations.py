# file: sketches/apps/animations.py
import time
import random

# Color Definitions
OFF = (0, 0, 0)
HEART_MASK = [0, 2, 3, 4, 5, 7]

def color_wheel(pos):
    if pos < 0 or pos > 255:
        return OFF
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

class Animations:
    def __init__(self, pixels):
        self.pixels = pixels
        self.modes = [
            ("Heartbeat Pulse", self.animate_heartbeat, 0.05),
            ("Rainbow Swirl", self.animate_rainbow, 0.02),
            ("Sparkle Mode", self.animate_sparkle, 0.1)
        ]

    def animate_heartbeat(self, step):
        brightness = int((1 + (step % 20 - 10) / 10.0) * 127)
        color = (brightness, 0, int(brightness / 2))
        self.pixels.fill(OFF)
        for idx in HEART_MASK:
            self.pixels[idx] = color
        self.pixels.show()

    def animate_rainbow(self, step):
        for i in range(9):
            pixel_index = (i * 256 // 9) + step
            self.pixels[i] = color_wheel(pixel_index & 255)
        self.pixels.show()

    def animate_sparkle(self, step):
        self.pixels.fill(OFF)
        active_pixel = random.randint(0, 8)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.pixels[active_pixel] = color
        self.pixels.show()

# End of file: sketches/apps/animations.py
