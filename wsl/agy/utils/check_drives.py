# file: agy/utils/check_drives.py
import subprocess
import json
import sys

def run_pwsh_command(cmd):
    try:
        # Wrap in subprocess.run as per AI.md guidelines to prevent hangs
        result = subprocess.run(
            ["pwsh.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def main():
    print("[*] Querying Windows host for volumes/drives...")
    stdout, stderr = run_pwsh_command("Get-Volume | Select-Object DriveLetter, FriendlyName, FileSystemType, Size, SizeRemaining | ConvertTo-Json")
    
    if not stdout.strip():
        print("[!] No volumes returned or output empty.")
        return
        
    try:
        data = json.loads(stdout)
        if isinstance(data, dict):
            data = [data]
            
        print(f"{'Drive':<6} {'Friendly Name':<25} {'Format':<8} {'Size (GB)':<10} {'Free (GB)':<10}")
        print("-" * 65)
        for vol in data:
            letter = vol.get("DriveLetter")
            if not letter:
                continue
            name = vol.get("FriendlyName") or ""
            fs = vol.get("FileSystemType") or ""
            size = vol.get("Size", 0)
            free = vol.get("SizeRemaining", 0)
            
            size_gb = f"{size / (1024**3):.2f}" if size else "N/A"
            free_gb = f"{free / (1024**3):.2f}" if free else "N/A"
            
            print(f"{letter + ':':<6} {name:<25} {fs:<8} {size_gb:<10} {free_gb:<10}")
            
    except Exception as e:
        print(f"Error parsing JSON output: {e}")
        print("Raw stdout:")
        print(stdout)

if __name__ == "__main__":
    main()
# End of file: agy/utils/check_drives.py
