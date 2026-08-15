<!-- file: AI.md -->
# Workspace Specification & Consolidated AI Directives (`AI.md`)

Notice to AI Agents: This document defines operational directives, environment boundaries, host interop protocols, and repository hygiene for all assistants operating within the `minifig-pi-aom` monorepo workspace.

---

## 1. System Topology & Environment Boundaries

- **Primary Repository:** `minifig-pi-aom` (`/home/fekerr/src/minifig-pi-aom`)
- **Dual-Environment Architecture:**
  - **WSL Guest:** Linux Bash environment under [`wsl/`](file:///home/fekerr/src/minifig-pi-aom/wsl/). Environment managed via local `.venv`. Always source [`wsl/config_env`](file:///home/fekerr/src/minifig-pi-aom/wsl/config_env).
  - **Windows Host:** Windows 11 64-bit Workstation under [`win11/`](file:///home/fekerr/src/minifig-pi-aom/win11/) (`C:\Users\feker\src\minifig-pi-aom\win11`).
- **Host Interop & Callouts:** Windows native functionality must be accessed via `pwsh.exe` (PowerShell 7+) rather than standard `powershell.exe`. Calls (e.g., `usbipd.exe` USB passthrough, host filesystem interop) should run via `pwsh.exe -NoProfile -ExecutionPolicy Bypass`.
- **Target Hardware Focus:** Minifig Pi (RP2040) running CircuitPython.
- **Microcontroller USB Drive:** Typically mounted at Windows host drive `D:\`.

---

## 2. Communication & Context Transfer Protocols

- **Heredoc Protocol:** Always quote heredoc delimiters (`cat << 'EOF' > file`) to prevent shell evaluation of variables and backticks in WSL.
- **Observability & Logging:** Collect and log both stdout and stderr. NEVER redirect standard output, standard error, stdin, or commands to/from NULL (e.g. `/dev/null`, `NUL`, `$null`) unless explicitly enabled by a human agent. Hide nothing.
- **Python-based Host Execution:** When running Windows host executables (such as `python.exe` or `pwsh.exe`) from WSL, always wrap them in Python's `subprocess.run(..., capture_output=True)` to prevent terminal/interactive hangs.

---

## 3. Formatting & Repository Hygiene

- **File Formatting:** Format all text files to ~80 columns as much as possible.
- **Source Code:** Standard formatting per language, keeping lines within 80–120 columns where practical.
- **Single-Line Copy-Paste Commands:** Format terminal commands on their own isolated single-line code blocks.
- **Mandatory File Headers & Footers:** All text files must have a header and footer.
  - Header: Every text file must begin with a comment specifying the file path:
    `<!-- file: relative/path/filename -->` or `# file: relative/path/filename`.
  - Footer: Every text file must end with a footer. The minimum footer format is:
    `<!-- End of file: relative/path/filename -->` or `# End of file: relative/path/filename`.

<!-- End of file: AI.md -->
