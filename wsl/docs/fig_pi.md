<!-- file: docs/fig_pi.md -->
# Fig Pi Microcontroller Board

The **Fig Pi** is a LEGO® minifigure-shaped development board based on the Raspberry Pi RP2040 microcontroller.

## Hardware Specifications
* **Microcontroller:** Raspberry Pi RP2040 (Dual-core ARM Cortex-M0+ at 133MHz)
* **Flash Memory:** 2MB onboard flash
* **Form Factor:** Minifigure shape (~0.95 × 1.55 inches)
* **Onboard Peripherals:**
  * 3×3 RGB addressable NeoPixel matrix (front)
  * Built-in red indicator LED (back)
  * RESET button
  * Programmable BOOT/User button
* **I/O & Expansion:**
  * 16 digital I/O pins (all PWM capable)
  * 4 analog inputs
  * STEMMA QT / QWIIC 4-pin JST SH connector (I2C)

## Firmware & Software
* **Default Runtime:** Ships preloaded with **Adafruit CircuitPython** (currently `8.1.0-beta.1` on this device).
* **Upload Mechanism:** UF2 bootloader (exposes a USB mass storage drive for drag-and-drop code replacement).

## Official Resources
* **Website:** [minifigboards.com](https://minifigboards.com)
* **GitHub (Creator - Ben Shockley):** [github.com/bwshockley](https://github.com/bwshockley)
* **Hardware Repositories:**
  * [Mini-SAM (SAMD51)](https://github.com/bwshockley/Mini-SAM)
  * [Minifigure-SAMD21E](https://github.com/bwshockley/Minifigure-SAMD21E)

<!-- End of file: docs/fig_pi.md -->
