# file: Makefile
# Purpose: Makefile to organize workspace tasks for Minifig WSL
# Target OS: Ubuntu 24.04 / 26.04 LTS (WSL2) + Windows 11 Host

.PHONY: help check clean

help:
	@echo "Available Makefile targets:"
	@echo "  make check  - Run status checks on the workspace"
	@echo "  make clean  - Clean temporary build/cache files"
	@echo "  make help   - Show this help menu"

check:
	@echo "[*] Checking Minifig WSL workspace..."
	@if [ -f config_env ]; then echo "[+] config_env present"; else echo "[!] config_env missing"; fi
	@if [ -f AI.md ]; then echo "[+] AI.md present"; else echo "[!] AI.md missing"; fi

clean:
	@echo "[*] Cleaning workspace..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# file Makefile ends
