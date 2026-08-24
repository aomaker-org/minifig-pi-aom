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
* **Default Runtime:** Ships preloaded with **Adafruit CircuitPython** (currently `8.1.0-beta.1` on this device). See [`firmware_updates.md`](file:///home/fekerr/src/minifig-pi-aom/wsl/docs/firmware_updates.md) for board specs and upgrade guides.
* **Upload Mechanism:** UF2 bootloader (exposes a USB mass storage drive for drag-and-drop code replacement).

## USB Drive Mounting & Filesystem Access
When the Minifig Pi is connected via USB, it exposes a mass storage filesystem (defaulting to the drive label `CIRCUITPY`).

### Windows Host
- Mounted automatically under a drive letter (typically `D:\`).

### WSL (Windows Subsystem for Linux)
Because WSL runs in a virtual machine, it cannot access Windows USB drives automatically. To access the drive:
1. **Mounting via DrvFs (Recommended for file access)**:
   ```bash
   sudo mkdir -p /mnt/d
   sudo mount -t drvfs D: /mnt/d
   ```
   This exposes the microcontroller files at `/mnt/d/`.
2. **USB IP Passthrough (`usbipd-win`) (For raw device/serial access)**:
   If you need direct serial communications or flashing via raw block devices:
   - On Windows (PowerShell 7+ as Administrator):
     ```powershell
     usbipd list
     usbipd bind --busid <BUSID>
     usbipd attach --wsl --busid <BUSID>
     ```
   - On WSL:
     Check with `lsusb` and mount the new block device (e.g., `/dev/sdb1`).

### Native Linux
- Mounted automatically by modern desktop environments under `/media/<username>/CIRCUITPY/`.
- For headless/manual mounting:
  ```bash
  sudo mkdir -p /mnt/circuitpy
  sudo mount /dev/sdb1 /mnt/circuitpy
  ```

## Official Resources
* **Website:** [minifigboards.com](https://minifigboards.com)
* **GitHub (Creator - Ben Shockley):** [github.com/bwshockley](https://github.com/bwshockley)
* **Hardware Repositories:**
  * [Mini-SAM (SAMD51)](https://github.com/bwshockley/Mini-SAM)
  * [Minifigure-SAMD21E](https://github.com/bwshockley/Minifigure-SAMD21E)

<!-- End of file: docs/fig_pi.md -->
