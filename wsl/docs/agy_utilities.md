<!-- file: docs/agy_utilities.md -->
# Antigravity (agy) host utilities

This document covers utility scripts used by `agy` to interface with the Windows 11 host and the connected Minifig microcontroller boards.

## Utilities

### 1. `check_drives.py`
* **Path:** [`agy/utils/check_drives.py`](file:///home/fekerr/src/minifig-wsl/agy/utils/check_drives.py)
* **Description:** Queries the Windows host via PowerShell (`pwsh.exe`) to list active logical drives, their file systems, total sizes, and remaining space.
* **Usage:**
  ```bash
  python3 agy/utils/check_drives.py
  ```

### 2. `sync_minifig.py`
* **Path:** [`agy/utils/sync_minifig.py`](file:///home/fekerr/src/minifig-wsl/agy/utils/sync_minifig.py)
* **Description:** A unified tool for diffing, backing up (pulling), or deploying (pushing) files between the local [`mirror/`](file:///home/fekerr/src/minifig-wsl/mirror) folder and the microcontroller's `D:\` drive on the host. It computes SHA256 hashes of files on both sides to only transfer modified or new files.
* **Usage:**
  * To inspect changes between the local mirror and the device:
    ```bash
    python3 agy/utils/sync_minifig.py diff
    ```
  * To backup files from the device to the local mirror:
    ```bash
    python3 agy/utils/sync_minifig.py pull
    ```
  * To deploy local mirror changes back to the device:
    ```bash
    python3 agy/utils/sync_minifig.py push
    ```

<!-- End of file: docs/agy_utilities.md -->
