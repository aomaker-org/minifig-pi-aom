# file: Makefile
# Purpose: Root Makefile to organize workspace tasks for minifig-pi-aom monorepo

.PHONY: help check clean

help:
	@echo "Available Makefile targets:"
	@echo "  make check  - Run status checks on the workspace"
	@echo "  make clean  - Clean temporary build/cache files"
	@echo "  make help   - Show this help menu"

check:
	@echo "[*] Checking minifig-pi-aom monorepo..."
	@if [ -f mirrors/manifest.toml ]; then echo "[+] mirrors/manifest.toml present"; else echo "[!] mirrors/manifest.toml missing"; fi
	@if [ -d wsl ]; then echo "[+] wsl/ directory present"; else echo "[!] wsl/ directory missing"; fi
	@if [ -d win11 ]; then echo "[+] win11/ directory present"; else echo "[!] win11/ directory missing"; fi

clean:
	@echo "[*] Cleaning workspace..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# End of file: Makefile
