# file: ps7/pipe2clip.ps1
# Purpose: Routes pipeline data to clipboard with overflow protection

[CmdletBinding()]
param (
    [Parameter(ValueFromPipeline = $true)]
    [string]$InputObject,
    
    [int]$MaxCharacters = 20480,
    [string]$LogDir = "C:\Users\feker\src\minifig-win11\logs"
)

begin {
    $Buffer = [System.Text.StringBuilder]::new()
}

process {
    if ($InputObject) {
        $null = $Buffer.AppendLine($InputObject)
    }
}

end {
    $FullText = $Buffer.ToString()
    if ([string]::IsNullOrWhiteSpace($FullText)) { return }
    
    if ($FullText.Length -le $MaxCharacters) {
        $FullText | clip.exe
    } else {
        if (-not (Test-Path $LogDir)) {
            New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
        }
        
        $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $FileName = "overflow_trace_${Timestamp}.log"
        $FileFullPath = Join-Path $LogDir $FileName
        
        [System.IO.File]::WriteAllText($FileFullPath, $FullText,
            [System.Text.Encoding]::UTF8)
        
        $Receipt = @(
            "[!] CLIPBOARD OVERFLOW PROTECTION ACTIVE",
            "----------------------------------------------------------------",
            "Output exceeded safety threshold ($($MaxCharacters) chars).",
            "Full trace dumped to disk.",
            "",
            "File Path: $FileFullPath",
            "File Size: $([Math]::Round($FullText.Length / 1KB, 2)) KB",
            "----------------------------------------------------------------"
        ) -join [System.Environment]::NewLine
        
        $Receipt | clip.exe
        Write-Host "[!] Large output. Pointer receipt copied to clipboard." `
            -ForegroundColor Yellow
    }
}

# End of file: ps7/pipe2clip.ps1
