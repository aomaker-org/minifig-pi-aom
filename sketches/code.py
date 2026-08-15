# file: sketches/code.py
import board
import time
import digitalio
import neopixel
import os
import sys
import supervisor
import microcontroller
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

# 1. Read Environment Configurations from settings.toml safely
active_mode_setting = str(os.getenv("ACTIVE_MODE", "all")).lower()

brightness_val = os.getenv("LED_BRIGHTNESS")
brightness_setting = float(brightness_val) if brightness_val is not None else 0.2

demo_duration_val = os.getenv("DEMO_DURATION")
demo_duration_setting = float(demo_duration_val) if demo_duration_val is not None else 30.0

fast_demo_duration_val = os.getenv("FAST_DEMO_DURATION")
fast_demo_duration_setting = float(fast_demo_duration_val) if fast_demo_duration_val is not None else 5.0

# Check for demo mode file triggers
fast_demo_active = file_exists("fast_demo_mode_on")
normal_demo_active = file_exists("demo_mode_on")

demo_mode_active = fast_demo_active or normal_demo_active
demo_duration = fast_demo_duration_setting if fast_demo_active else demo_duration_setting

print(f"[Config] ACTIVE_MODE: {active_mode_setting}")
print(f"[Config] LED_BRIGHTNESS: {brightness_setting}")
print(f"[Config] DEMO_MODE: {demo_mode_active} (Normal: {normal_demo_active}, Fast: {fast_demo_active})")
print(f"[Config] DEMO_DURATION: {demo_duration}s")

# 2. Initialize Hardware Safely
led_pin = getattr(board, "LED", None)
if led_pin is not None:
    led = digitalio.DigitalInOut(led_pin)
    led.direction = digitalio.Direction.OUTPUT
    print("[HW] Built-in LED initialized")
else:
    led = None
    print("[HW] Warning: board.LED not found")

button_pin = getattr(board, "BUTTON", None)
if button_pin is not None:
    button = digitalio.DigitalInOut(button_pin)
    button.switch_to_input(pull=digitalio.Pull.UP)
    print("[HW] User button initialized")
else:
    button = None
    print("[HW] Warning: board.BUTTON not found")

neopixel_pin = getattr(board, "NEOPIXEL", None)
if neopixel_pin is None:
    neopixel_pin = microcontroller.pin.GPIO13
    print("[HW] board.NEOPIXEL not found. Falling back to GPIO13")
else:
    print("[HW] board.NEOPIXEL found")

pixels = neopixel.NeoPixel(neopixel_pin, 9, brightness=brightness_setting, auto_write=False)

# Custom color state for Web Control Mode
custom_web_colors = [(0, 0, 0)] * 9

def render_web_control(step):
    for i in range(9):
        pixels[i] = custom_web_colors[i]
    pixels.show()

# 3. Instantiate Sub-apps
anim_app = Animations(pixels)
diag_app = Diagnostics(pixels, led, button) if led and button else None

# Helper function to dynamically rebuild loaded modes list
def rebuild_active_modes():
    global active_modes, current_mode_idx
    active_modes = []
    
    # Animations
    if active_mode_setting in ["animations", "all"]:
        active_modes.extend(anim_app.modes)
    # Diagnostics
    if diag_app and active_mode_setting in ["diagnostics", "all"]:
        active_modes.extend(diag_app.modes)
        
    # Always append Web Control Mode as the last mode
    web_control_mode = ("Web Control Mode", render_web_control, 0.05)
    active_modes.append(web_control_mode)
    
    # Ensure current mode index is valid
    if current_mode_idx >= len(active_modes):
        current_mode_idx = 0

# Initial build
active_modes = []
current_mode_idx = 0
rebuild_active_modes()

print(f"[+] Loaded {len(active_modes)} active modes:")
for idx, (name, _, _) in enumerate(active_modes):
    print(f"  Mode {idx}: {name}")

# Event Loop variables
step = 0
last_button_state = True
last_mode_switch_time = time.monotonic()

while True:
    mode_name, render_func, delay = active_modes[current_mode_idx]
    current_time = time.monotonic()
    
    # 4. Non-blocking Serial Input Check (WebSerial commands)
    if supervisor.runtime.serial_bytes_available:
        try:
            line = sys.stdin.readline().strip()
            
            # GET_TEMP -> returns CPU temperature
            if line == "GET_TEMP":
                temp = microcontroller.cpu.temperature
                print(f"TEMP:{temp:.2f}")
                
            # SET_MODE:<idx> -> switch to animation/diagnostic mode
            elif line.startswith("SET_MODE:"):
                target_idx = int(line.split(":", 1)[1])
                if 0 <= target_idx < len(active_modes):
                    current_mode_idx = target_idx
                    last_mode_switch_time = current_time
                    step = 0
                    print(f"MODE_ACTIVE:{current_mode_idx}")
                    
            # SET_COLOR:<index>:<r>,<g>,<b> -> set specific pixel color
            elif line.startswith("SET_COLOR:"):
                _, p_idx_str, rgb_str = line.split(":")
                p_idx = int(p_idx_str)
                r, g, b = map(int, rgb_str.split(","))
                if 0 <= p_idx < 9:
                    custom_web_colors[p_idx] = (r, g, b)
                    web_idx = len(active_modes) - 1
                    if current_mode_idx != web_idx:
                        current_mode_idx = web_idx
                        print(f"MODE_ACTIVE:{web_idx}")
                        
            # GET_MODES -> returns list of loaded modes
            elif line == "GET_MODES":
                mode_names = ",".join([m[0] for m in active_modes])
                print(f"MODES:{mode_names}")
                
            # TOGGLE_DEMO:ON/OFF -> toggle auto loop cycling
            elif line.startswith("TOGGLE_DEMO:"):
                state = line.split(":", 1)[1]
                demo_mode_active = (state == "ON")
                last_mode_switch_time = current_time
                print(f"DEMO_STATUS:{'ON' if demo_mode_active else 'OFF'}")
                
            # SET_DURATION:<val> -> change cycle interval
            elif line.startswith("SET_DURATION:"):
                val = float(line.split(":", 1)[1])
                demo_duration = val
                last_mode_switch_time = current_time
                print(f"DEMO_DURATION_SET:{demo_duration}")
                
            # SET_ACTIVE_MODE:all/animations/diagnostics -> rebuild group
            elif line.startswith("SET_ACTIVE_MODE:"):
                mode_group = line.split(":", 1)[1].lower()
                if mode_group in ["all", "animations", "diagnostics"]:
                    active_mode_setting = mode_group
                    rebuild_active_modes()
                    print(f"ACTIVE_GROUP_SET:{active_mode_setting}")
                    # Notify the web client to reload the button list
                    mode_names = ",".join([m[0] for m in active_modes])
                    print(f"MODES:{mode_names}")
                    print(f"MODE_ACTIVE:{current_mode_idx}")
                    
            # GET_STATUS -> send current configurations
            elif line == "GET_STATUS":
                print(f"DEMO_STATUS:{'ON' if demo_mode_active else 'OFF'}")
                print(f"DEMO_DURATION_SET:{demo_duration}")
                print(f"ACTIVE_GROUP_SET:{active_mode_setting}")
                print(f"MODE_ACTIVE:{current_mode_idx}")
                
        except Exception as e:
            pass
            
    # Check for automatic demo mode switch
    if demo_mode_active and (current_time - last_mode_switch_time >= demo_duration):
        if mode_name != "Web Control Mode":
            # Cycle through all loaded modes except the last one (Web Control Mode)
            current_mode_idx = (current_mode_idx + 1) % (len(active_modes) - 1)
            last_mode_switch_time = current_time
            print(f"[*] Demo Mode Auto-Switch to: {active_modes[current_mode_idx][0]}")
            # Notify web client of switch
            print(f"MODE_ACTIVE:{current_mode_idx}")
            if led:
                led.value = True
                time.sleep(0.1)
                led.value = False
            step = 0
            continue
        
    # Read button if present (Active Low)
    if button:
        button_pressed = not button.value
        if button_pressed and last_button_state:
            current_mode_idx = (current_mode_idx + 1) % len(active_modes)
            last_mode_switch_time = current_time
            print(f"[*] Switching to Mode {current_mode_idx}: {active_modes[current_mode_idx][0]}")
            print(f"MODE_ACTIVE:{current_mode_idx}")
            
            if led:
                for _ in range(3):
                    led.value = True
                    time.sleep(0.08)
                    led.value = False
                    time.sleep(0.08)
            time.sleep(0.2) # debounce
            step = 0
            
        last_button_state = not button_pressed
    
    # Toggle built-in LED state every cycle as a heartbeat indicator
    heartbeat_rate = 40 if demo_mode_active else 20
    if led and step % heartbeat_rate == 0 and "Test" not in mode_name:
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
