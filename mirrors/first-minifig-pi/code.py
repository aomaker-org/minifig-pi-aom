# file: mirror/code.py
import board
import time
import digitalio
import neopixel
import random

print("--- Minifig Interactive NeoPixel Demo ---")

# 1. Initialize Built-in LED (GPIO0)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# 2. Initialize Built-in Button (GPIO20) - Active Low
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# 3. Initialize 3x3 NeoPixel Matrix (GPIO13, 9 pixels)
# Auto-write is disabled for smoother custom rendering animations
pixels = neopixel.NeoPixel(board.NEOPIXEL, 9, brightness=0.2, auto_write=False)

# Color Definitions
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# Helper function to generate rainbow color wheel
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

# 1. Mode: Heartbeat Pulse (pulse a heart shape in the 3x3 grid)
# Heart shape mask for 3x3:
#  * . *
#  * * *
#  . * .
# Pixel indices in 3x3 grid:
#  0 1 2
#  3 4 5
#  6 7 8
HEART_MASK = [0, 2, 3, 4, 5, 7]

def animate_heartbeat(step):
    brightness = int((1 + (step % 20 - 10) / 10.0) * 127) # pulsating 0-254
    color = (brightness, 0, int(brightness / 2)) # pulsing pinkish/red
    
    pixels.fill(OFF)
    for idx in HEART_MASK:
        pixels[idx] = color
    pixels.show()
    time.sleep(0.05)

# 2. Mode: Rainbow Swirl
def animate_rainbow(step):
    for i in range(9):
        # Offset colors across the 9 pixels
        pixel_index = (i * 256 // 9) + step
        pixels[i] = color_wheel(pixel_index & 255)
    pixels.show()
    time.sleep(0.02)

# 3. Mode: Sparkle Mode
def animate_sparkle(step):
    pixels.fill(OFF)
    # Pick a random pixel to light up with a random color
    active_pixel = random.randint(0, 8)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    pixels[active_pixel] = color
    pixels.show()
    time.sleep(0.1)

# Animation Control State
mode = 0
num_modes = 3
step = 0
last_button_state = True

print("Demo started. Press the USER/BOOT button to change modes!")

while True:
    # Read button value (False when pressed)
    button_pressed = not button.value
    
    # Toggle mode on press (falling edge detection)
    if button_pressed and last_button_state:
        mode = (mode + 1) % num_modes
        print(f"[*] Mode changed to: {mode}")
        # Blink built-in LED to confirm mode change
        for _ in range(3):
            led.value = True
            time.sleep(0.08)
            led.value = False
            time.sleep(0.08)
        time.sleep(0.2) # debounce delay
        
    last_button_state = not button_pressed
    
    # Toggle built-in LED state every cycle as a heartbeat indicator
    if step % 20 == 0:
        led.value = not led.value
        
    # Execute current animation mode
    if mode == 0:
        animate_heartbeat(step)
    elif mode == 1:
        animate_rainbow(step)
    elif mode == 2:
        animate_sparkle(step)
        
    step = (step + 1) % 10000
# End of file: mirror/code.py
