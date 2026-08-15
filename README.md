<!-- file: README.md -->
# Minifig Pi Aomaker-Org Workspace (`minifig-pi-aom`)

This repository consolidates all environment setups, tools, and code mirrors for developing and managing Minifig microcontroller boards (such as the Fig Pi and Mini SAM) under `aomaker-org`.

## Repository Structure

* **[`mirrors/`](file:///home/fekerr/src/minifig-pi-aom/mirrors/):** Device mirrors containing actual files currently active on microcontrollers, indexed by hardware ID in `mirrors/manifest.toml`.
* **[`wsl/`](file:///home/fekerr/src/minifig-pi-aom/wsl/):** Ubuntu WSL2 specific environment setups, scripts, and utilities.
* **[`win11/`](file:///home/fekerr/src/minifig-pi-aom/win11/):** Windows host-side settings and tools (e.g. PowerShell utilities in `win11/ps7/`).

## Quick Start (WSL Side)

1. Load your local WSL environment:
   ```bash
   source wsl/config_env
   ```
2. Interact with the connected Minifig microcontroller:
   ```bash
   # Compare files on device D: drive against local mirrors/
   python3 wsl/agy/utils/sync_minifig.py diff

   # Backup device files to mirrors/
   python3 wsl/agy/utils/sync_minifig.py pull

   # Push changes from mirrors/ to device
   python3 wsl/agy/utils/sync_minifig.py push
   ```

<!-- End of file: README.md -->
