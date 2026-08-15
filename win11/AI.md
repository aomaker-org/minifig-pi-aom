# Workspace Specification & Consolidated AI Directives (`AI.md`)
<!-- file: AI.md -->

Notice to AI Agents: This document defines operational directives, environment boundaries, and repository hygiene for all assistants operating within the Windows-native `minifig-win11` workspace.

---

## 1. System Topology & Environment Boundaries

- **Primary Repository:** `minifig-win11` (`C:\Users\feker\src\minifig-win11`)
- **Primary Host Runtime:** Windows 11 64-bit Workstation Architecture
- **Host PowerShell:** Standard shell command execution must use `pwsh.exe` (PowerShell 7+) rather than standard `powershell.exe`.
- **Target Hardware Focus:** Minifig Boards (e.g. Fig Pi with RP2040, Mini SAM M4 with ATSAMD51G19A) supporting CircuitPython, MicroPython, and Arduino.
- **Microcontroller USB Drive:** Typically mounted at host drive `D:\` (`CIRCUITPY`).

---

## 2. Communication & Context Transfer Protocols

- **Observability & Logging:** Collect and log both stdout and stderr. NEVER redirect standard output, standard error, stdin, or commands to/from NULL (e.g. `NUL`, `$null`, `/dev/null`) unless explicitly enabled by a human agent. Hide nothing.

---

## 3. Formatting & Repository Hygiene

- **File Formatting:** Format all text files to ~80 columns as much as possible.
- **Source Code:** Standard formatting per language, keeping lines within 80–120 columns where practical.
- **Mandatory File Headers & Footers:** All text files must have a header and footer.
  - Header: Every text file must begin with a comment specifying the file path:
    `<!-- file: relative/path/filename -->` or `# file: relative/path/filename`.
  - Footer: Every text file must end with a footer. The minimum footer format is:
    `<!-- End of file: relative/path/filename -->` or `# End of file: relative/path/filename`.

<!-- End of file: AI.md -->
