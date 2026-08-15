# file: sketches/code.py
import board
import time
import digitalio
import neopixel
import os
from apps.animations import Animations
from apps.diagnostics import Diagnostics

print("--- Minifig Unified Dispatcher Booting ---")

# Helper to check file existence in CircuitPython
def file_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

# 1. Read Environment Configurations from settings.toml
active_mode_setting = os.getenv("ACTIVE_MODE", "all").lower()
brightness_setting = float(os.getenv("LED_BRIGHTNESS", 0.2))
demo_duration_setting = float(os.getenv("DEMO_DURATION", 30.0))
fast_demo_duration_setting = float(os.getenv("FAST_DEMO_DURATION", 5.0))

# Check for demo mode file triggers
fast_demo_active = file_exists("fast_demo_mode_on")
normal_demo_active = file_exists("demo_mode_on")

demo_mode_active = fast_demo_active or normal_demo_active
demo_duration = fast_demo_duration_setting if fast_demo_active else demo_duration_setting

print(f"[Config] ACTIVE_MODE: {active_mode_setting}")
print(f"[Config] LED_BRIGHTNESS: {brightness_setting}")
print(f"[Config] DEMO_MODE: {demo_mode_active} (Normal: {normal_demo_active}, Fast: {fast_demo_active})")
print(f"[Config] DEMO_DURATION: {demo_duration}s")

# 2. Initialize Hardware
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 9, brightness=brightness_setting, auto_write=False)

# 3. Instantiate Sub-apps
anim_app = Animations(pixels)
diag_app = Diagnostics(pixels, led, button)

# 4. Assemble Mode List based on settings.toml config
active_modes = []

if active_mode_setting in ["animations", "all"]:
    active_modes.extend(anim_app.modes)
if active_mode_setting in ["diagnostics", "all"]:
    active_modes.extend(diag_app.modes)

# Fallback in case configuration is invalid
if not active_modes:
    print("[!] Warning: Invalid ACTIVE_MODE. Defaulting to all.")
    active_modes.extend(anim_app.modes)
    active_modes.extend(diag_app.modes)

print(f"[+] Loaded {len(active_modes)} active modes:")
for idx, (name, _, _) in enumerate(active_modes):
    print(f"  Mode {idx}: {name}")

# Event Loop variables
current_mode_idx = 0
step = 0
last_button_state = True
last_mode_switch_time = time.monotonic()

while True:
    mode_name, render_func, delay = active_modes[current_mode_idx]
    current_time = time.monotonic()
    
    # Check for automatic demo mode switch
    if demo_mode_active and (current_time - last_mode_switch_time >= demo_duration):
        current_mode_idx = (current_mode_idx + 1) % len(active_modes)
        last_mode_switch_time = current_time
        print(f"[*] Demo Mode Auto-Switch to: {active_modes[current_mode_idx][0]}")
        # Blink built-in LED to confirm auto-switch
        led.value = True
        time.sleep(0.1)
        led.value = False
        step = 0
        continue
        
    # Read button (Active Low)
    button_pressed = not button.value
    
    # Switch mode on button press (falling edge detection)
    if button_pressed and last_button_state:
        current_mode_idx = (current_mode_idx + 1) % len(active_modes)
        last_mode_switch_time = current_time # Reset timer on manual override
        print(f"[*] Switching to Mode {current_mode_idx}: {mode_name}")
        
        # Blink built-in LED to confirm switch
        for _ in range(3):
            led.value = True
            time.sleep(0.08)
            led.value = False
            time.sleep(0.08)
        time.sleep(0.2) # debounce
        step = 0 # reset animation steps
        
    last_button_state = not button_pressed
    
    # Toggle built-in LED state every cycle as a heartbeat indicator (if not overridden by diagnostics)
    # Slow heartbeat in demo mode, faster in normal mode
    heartbeat_rate = 40 if demo_mode_active else 20
    if step % heartbeat_rate == 0 and "Test" not in mode_name:
        led.value = not led.value
        
    # Run the active animation step
    try:
        render_func(step)
    except Exception as e:
        print(f"[!] Error rendering {mode_name}: {e}")
        time.sleep(1.0)
        
    time.sleep(delay)
    step = (step + 1) % 10000
# End of file: sketches/code.py
