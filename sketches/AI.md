<!-- file: sketches/AI.md -->
# Minifig Pi Build Metadata & Attributions

## Build Details
* **Firmware Version:** 1.2.0 (Dynamic Brightness & Loop Filters Release)
* **Sync Timestamp:** 2026-08-16T08:26:49-07:00
* **Assistant Environment:** Antigravity 2.0 / agy CLI / Gemini Pro

## Hardware Attributions
* **Target Board:** bwshockley_figpi (RP2040)
* **Onboard Matrix:** 3x3 NeoPixel Matrix (GP13)
* **Heartbeat Indicator:** Onboard LED (GP0)
* **Switch Interface:** Physical Button (GP20, active-low)
* **Virtual Console:** USB CDC Serial (115200 baud, DTR/RTS)

## Software Stack
* **Language:** Adafruit CircuitPython 8.1.0-beta.1
* **External Modules:** `adafruit_neopixel` (lib/neopixel.py)
* **Local Control:** web_control.html (WebSerial API dashboard + Chart.js telemetry)

<!-- End of file: sketches/AI.md -->
