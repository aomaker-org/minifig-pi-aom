<!-- file: README.md -->
# Minifig WSL Workspace

Welcome to the `minifig-wsl` development environment. This workspace is configured for developing and managing code running on Minifig microcontroller boards (such as the Fig Pi) from within Windows Subsystem for Linux (WSL2).

## Documentation

* **[`docs/fig_pi.md`](file:///home/fekerr/src/minifig-wsl/docs/fig_pi.md):** Hardware specifications, firmware details, and references for the Fig Pi (RP2040) board.
* **[`docs/agy_utilities.md`](file:///home/fekerr/src/minifig-wsl/docs/agy_utilities.md):** Guide to the local host integration tools and sync script (`sync_minifig.py`).
* **[`AI.md`](file:///home/fekerr/src/minifig-wsl/AI.md):** Workspace rules and environment boundary configuration for AI assistants.

## Quick Start (Synchronizing Files)

You can check changes, back up files from the board, or push local changes to the board using the sync utility:

```bash
# Check difference between local mirror/ and device D: drive
python3 agy/utils/sync_minifig.py diff

# Pull/Backup files from device to local mirror/
python3 agy/utils/sync_minifig.py pull

# Push/Deploy files from local mirror/ to device
python3 agy/utils/sync_minifig.py push
```

<!-- End of file: README.md -->
