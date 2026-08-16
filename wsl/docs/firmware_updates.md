<!-- file: wsl/docs/firmware_updates.md -->
# CircuitPython Firmware Updates & Status

This document logs the current microcontroller firmware specs, update availability, and instructions for upgrading the board.

## Current Device Info
* **Board Name:** Fig Pi
* **Microcontroller:** Raspberry Pi RP2040
* **Board ID:** `bwshockley_figpi`
* **UID:** `E662086543252A2A`
* **Installed Version:** `8.1.0-beta.1`
* **Build Date:** 2023-03-30

## Available Upgrades (Backlog)
* **Stable Release:** `10.2.1`
* **Development Release:** `10.3.0-alpha.4`
* **Official Downloads:** [circuitpython.org/board/bwshockley_figpi/](https://circuitpython.org/board/bwshockley_figpi/)

## How to Flash New Firmware
1. **Enter Bootloader Mode:**
   * Connect the Fig Pi to your PC using a micro-USB/USB-C data cable.
   * Press and hold the physical **BOOT/User** button on the back of the board, then press and release the **RESET** button (or unplug/replug the USB cable while holding BOOT).
   * Release the BOOT button.
2. **Copy UF2 File:**
   * A new drive named `RPI-RP2` will appear on your Windows Host.
   * Download the desired `.uf2` firmware file from circuitpython.org.
   * Drag and drop the `.uf2` file onto the `RPI-RP2` drive.
3. **Automatic Reboot:**
   * The board will automatically reboot, flash the new firmware, and mount again as a `CIRCUITPY` drive (or `D:\` drive).
4. **Re-sync Files:**
   * Once the upgrade is complete, re-run our synchronization tool from WSL to restore all custom sketches and libraries:
     ```bash
     python3 wsl/agy/utils/sync_minifig.py push
     ```

<!-- End of file: wsl/docs/firmware_updates.md -->
