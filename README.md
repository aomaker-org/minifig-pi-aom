<!-- file: README.md -->
# Minifig Pi Aomaker-Org Workspace (`minifig-pi-aom`)

This repository consolidates all environment setups, tools, and code mirrors for developing and managing the Minifig Pi microcontroller under `aomaker-org`.

## Repository Structure

* **[`wsl/docs/fig_pi.md`](file:///home/fekerr/src/minifig-pi-aom/wsl/docs/fig_pi.md):** Hardware specifications, firmware details, and references for the Fig Pi (RP2040) board.
* **[`wsl/docs/agy_utilities.md`](file:///home/fekerr/src/minifig-pi-aom/wsl/docs/agy_utilities.md):** Guide to the local host integration tools and sync script (`sync_minifig.py`).
* **[`wsl/docs/backlog.md`](file:///home/fekerr/src/minifig-pi-aom/wsl/docs/backlog.md):** Future roadmap, experimental USB capabilities, and backup backlog items.
* **[`AI.md`](file:///home/fekerr/src/minifig-pi-aom/AI.md):** Workspace rules and environment boundary configuration for AI assistants.

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
