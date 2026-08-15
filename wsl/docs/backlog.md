<!-- file: wsl/docs/backlog.md -->
# Project Backlog & Future Ideas

This document tracks planned features, enhancements, and experimental integrations for the `minifig-pi-aom` workspace.

## Feature Backlog

### 1. Host Telemetry via USB CDC Serial
* **Description:** Stream Windows host metrics (CPU load, RAM usage, CPU temperature) to the Fig Pi using a host-side Python service (`pyserial`) and render them on the 3×3 NeoPixel matrix.
* **Status:** Drafted.

### 2. USB HID Macro Controller
* **Description:** Configure the Fig Pi to emulate a USB Human Interface Device (HID). Leverage the onboard user button as a macro key to trigger host actions (e.g. mute mic, screen lock, run a script).
* **Status:** Drafted.

### 3. Automated `rclone` Backups
* **Description:** Integrate `rclone` in the sync scripts to automatically back up local device mirrors (`mirrors/`) to Google Drive or other remote cloud storage providers.
* **Status:** Drafted.

### 4. WebUSB Control Dashboard
* **Description:** Build a lightweight HTML/JS web panel that leverages Chrome WebUSB/WebSerial to configure NeoPixel animations and settings directly from a web page.
* **Status:** Drafted.

<!-- End of file: wsl/docs/backlog.md -->
