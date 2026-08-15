# file: Makefile
# Purpose: Makefile to organize workspace tasks for Minifig Win11
# Target OS: Windows 11 Host

.PHONY: help check clean

help:
	@echo "Available Makefile targets:"
	@echo "  make check  - Run status checks on the workspace"
	@echo "  make clean  - Clean temporary build/cache files"
	@echo "  make help   - Show this help menu"

check:
	@echo "[*] Checking Minifig Win11 workspace..."
	@if exist AI.md (echo [+] AI.md present) else (echo [!] AI.md missing)

clean:
	@echo "[*] Cleaning workspace..."
	@if exist .ruff_cache rmdir /s /q .ruff_cache

# file Makefile ends
