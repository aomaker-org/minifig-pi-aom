# file: agy/utils/sync_minifig.py
import os
import sys
import json
import base64
import hashlib
import subprocess
import argparse

def run_pwsh_command(cmd):
    try:
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
        return None, None

def get_device_info():
    """Reads boot_out.txt from device to fetch board_id and UID."""
    stdout, _ = run_pwsh_command("if (Test-Path D:\\boot_out.txt) { Get-Content -Path D:\\boot_out.txt -Raw }")
    if not stdout or not stdout.strip():
        return None, None
    board_id = None
    uid = None
    for line in stdout.splitlines():
        if line.startswith("Board ID:"):
            board_id = line.split(":", 1)[1].strip()
        elif line.startswith("UID:"):
            uid = line.split(":", 1)[1].strip()
    return board_id, uid

def load_manifest(manifest_path):
    devices = {}
    if not os.path.exists(manifest_path):
        return devices
    current_uid = None
    with open(manifest_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[devices.") and line.endswith("]"):
                current_uid = line[9:-1].strip()
                devices[current_uid] = {}
            elif "=" in line and current_uid:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                devices[current_uid][key] = val
    return devices

def save_manifest(manifest_path, devices):
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    with open(manifest_path, "w") as f:
        f.write("# file: mirrors/manifest.toml\n")
        f.write("# Manifest mapping microcontroller UIDs to friendly mirror folders and settings\n\n")
        for uid, fields in devices.items():
            f.write(f"[devices.{uid}]\n")
            for k, v in fields.items():
                f.write(f'{k} = "{v}"\n')
            f.write("\n")
        f.write("# End of file: mirrors/manifest.toml\n")

def get_device_files():
    """Queries Windows host for files on D:\\ along with their size and SHA256 hash."""
    cmd = (
        "Get-ChildItem -Path D:\\ -Recurse -File | ForEach-Object { "
        "  $h = Get-FileHash -Path $_.FullName -Algorithm SHA256; "
        "  [PSCustomObject]@{ Path=$_.FullName; Hash=$h.Hash; Size=$_.Length } "
        "} | ConvertTo-Json"
    )
    stdout, _ = run_pwsh_command(cmd)
    if not stdout or not stdout.strip():
        return {}
        
    try:
        data = json.loads(stdout)
        if isinstance(data, dict):
            data = [data]
    except Exception:
        return {}

    device_files = {}
    for entry in data:
        win_path = entry.get("Path")
        if not win_path or not win_path.startswith("D:\\"):
            continue
        rel_path = win_path[3:].replace("\\", "/")
        device_files[rel_path] = {
            "win_path": win_path,
            "hash": entry.get("Hash").lower(),
            "size": entry.get("Size")
        }
    return device_files

def get_local_files(mirror_dir):
    """Scan local mirror directory and calculate size and SHA256 hash for each file."""
    local_files = {}
    if not os.path.exists(mirror_dir):
        return local_files
        
    for root, _, filenames in os.walk(mirror_dir):
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, mirror_dir).replace("\\", "/")
            
            sha256 = hashlib.sha256()
            try:
                with open(abs_path, "rb") as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)
                file_hash = sha256.hexdigest().lower()
                size = os.path.getsize(abs_path)
                local_files[rel_path] = {
                    "abs_path": abs_path,
                    "hash": file_hash,
                    "size": size
                }
            except Exception as e:
                print(f"[!] Failed to hash local file {rel_path}: {e}")
                
    return local_files

def compare_files(local, device):
    all_paths = set(local.keys()).union(device.keys())
    comparison = []
    
    for path in sorted(all_paths):
        loc = local.get(path)
        dev = device.get(path)
        
        if loc and not dev:
            status = "Local Only"
        elif dev and not loc:
            status = "Device Only"
        elif loc["hash"] != dev["hash"]:
            status = "Modified"
        else:
            status = "Identical"
            
        comparison.append({
            "path": path,
            "status": status,
            "local": loc,
            "device": dev
        })
    return comparison

def show_diff(comparison):
    print(f"\n{'Status':<15} {'File Path':<50}")
    print("-" * 70)
    for item in comparison:
        if item["status"] != "Identical":
            print(f"{item['status']:<15} {item['path']:<50}")
    
    identical_count = sum(1 for item in comparison if item["status"] == "Identical")
    print(f"\n[+] {identical_count} files are identical.")

def pull_files(comparison, mirror_dir):
    os.makedirs(mirror_dir, exist_ok=True)
    pulled = 0
    for item in comparison:
        if item["status"] in ["Device Only", "Modified"]:
            rel_path = item["path"]
            win_path = item["device"]["win_path"]
            local_path = os.path.join(mirror_dir, rel_path)
            
            print(f"[*] Pulling {win_path} -> {local_path}...")
            read_cmd = f"[Convert]::ToBase64String([System.IO.File]::ReadAllBytes('{win_path}'))"
            b64_out, _ = run_pwsh_command(read_cmd)
            
            if not b64_out:
                print(f"[!] Error reading {win_path} from device")
                continue
                
            try:
                file_bytes = base64.b64decode(b64_out.strip())
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(file_bytes)
                pulled += 1
            except Exception as e:
                print(f"[!] Error saving {rel_path}: {e}")
                
    print(f"[+] Successfully pulled {pulled} files.")

def push_files(comparison, mirror_dir):
    pushed = 0
    for item in comparison:
        if item["status"] in ["Local Only", "Modified"]:
            rel_path = item["path"]
            local_path = item["local"]["abs_path"]
            win_path = f"D:\\{rel_path.replace('/', '\\')}"
            
            print(f"[*] Pushing {local_path} -> {win_path}...")
            
            try:
                with open(local_path, "rb") as f:
                    b64_data = base64.b64encode(f.read()).decode("utf-8")
            except Exception as e:
                print(f"[!] Error reading local file {rel_path}: {e}")
                continue
                
            rel_dir = os.path.dirname(rel_path)
            if rel_dir:
                win_dir = f"D:\\{rel_dir.replace('/', '\\')}"
                mkdir_cmd = f"New-Item -ItemType Directory -Force -Path '{win_dir}'"
                run_pwsh_command(mkdir_cmd)
                
            write_cmd = f"[System.IO.File]::WriteAllBytes('{win_path}', [System.Convert]::FromBase64String('{b64_data}'))"
            _, err = run_pwsh_command(write_cmd)
            
            if err and err.strip():
                print(f"[!] Potential issue pushing {rel_path}: {err.strip()}")
            else:
                pushed += 1
                
    print(f"[+] Successfully pushed {pushed} files.")

def main():
    parser = argparse.ArgumentParser(description="Sync/Diff utility for Minifig CircuitPython drive")
    parser.add_argument("action", choices=["diff", "pull", "push"], help="Action to perform")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    manifest_path = os.path.join(repo_root, "mirrors/manifest.toml")
    
    print("[*] Detecting connected Minifig microcontroller...")
    board_id, uid = get_device_info()
    
    if not uid:
        print("[!] Error: Could not detect microcontroller or D:\\boot_out.txt is missing.")
        sys.exit(1)
        
    print(f"[+] Detected board: {board_id} (UID: {uid})")
    
    # Load manifest and determine local mirror directory
    devices = load_manifest(manifest_path)
    
    if uid not in devices:
        friendly_name = f"device-{uid[-6:].lower()}"
        print(f"[*] New device detected. Registering as '{friendly_name}' in manifest...")
        devices[uid] = {
            "board_id": board_id,
            "friendly_name": friendly_name,
            "mirror_path": f"mirrors/{friendly_name}",
            "comment": f"Auto-registered board (UID: {uid})"
        }
        save_manifest(manifest_path, devices)
        
    device_config = devices[uid]
    mirror_dir = os.path.join(repo_root, device_config["mirror_path"])
    print(f"[+] Using local mirror folder: {mirror_dir} ({device_config['friendly_name']})")
    
    print("[*] Scanning local mirror directory...")
    local = get_local_files(mirror_dir)
    
    print("[*] Scanning Minifig device (D: drive)...")
    device = get_device_files()
    
    comparison = compare_files(local, device)
    
    if args.action == "diff":
        show_diff(comparison)
    elif args.action == "pull":
        pull_files(comparison, mirror_dir)
    elif args.action == "push":
        push_files(comparison, mirror_dir)

if __name__ == "__main__":
    main()
# End of file: agy/utils/sync_minifig.py
