# file: query_registry_com.py
import subprocess

def run_pwsh(cmd):
    try:
        result = subprocess.run(
            ["pwsh.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), ""
    except subprocess.CalledProcessError as e:
        return None, f"Error: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}"

def main():
    print("[*] Listing serial port mappings in Windows Registry...")
    cmd = (
        "$res = Get-ItemProperty -Path 'HKLM:\\HARDWARE\\DEVICEMAP\\SERIALCOMM'; "
        "foreach ($prop in $res.psobject.properties) { "
        "  if ($prop.MemberType -eq 'NoteProperty') { "
        "    Write-Output ($prop.Name + ' = ' + $prop.Value) "
        "  } "
        "}"
    )
    out, err = run_pwsh(cmd)
    if out:
        print("[+] Serial ports mapped:")
        print(out)
    else:
        print(f"[!] Registry query failed: {err}")

if __name__ == "__main__":
    main()
# End of file: query_registry_com.py
