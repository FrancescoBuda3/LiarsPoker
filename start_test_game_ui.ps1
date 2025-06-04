param (
    [int]$clients_number,
    [string]$debuggable = "_"
)

if (-not $clients_number) {
    Write-Host "Usage: .\start_clients.ps1 <clients_number> <debug>"
    exit 1
}


if ($debuggable -eq "d") {
    Write-Host "Debug mode enabled"
    $debuggable = "-d"
}

$mosquitto1 = Get-Process -Name "mosquitto1" -ErrorAction SilentlyContinue
$mosquitto2 = Get-Process -Name "mosquitto2" -ErrorAction SilentlyContinue

if (-not $mosquitto1) {
    Write-Host "Starting primary Mosquitto (1883)..."
    if ($debuggable -eq "-d") {
        $mosquitto1 = Start-Process -PassThru -WindowStyle Hidden -FilePath "mosquitto" -ArgumentList "-c", "src/config/mosquitto1.conf", "-v"
    } else {
        $mosquitto1 = Start-Process -PassThru -WindowStyle Hidden -FilePath "mosquitto" -ArgumentList "-c", "src/config/mosquitto1.conf"
    }
} else {
    Write-Host "Primary Mosquitto already running."
}

if (-not $mosquitto2) {
    Write-Host "Starting backup Mosquitto (1884)..."
    if ($debuggable -eq "-d") {
        $mosquitto2 = Start-Process -PassThru -WindowStyle Hidden -FilePath "mosquitto" -ArgumentList "-c", "src/config/mosquitto2.conf", "-v"
    } else {
        $mosquitto2 = Start-Process -PassThru -WindowStyle Hidden -FilePath "mosquitto" -ArgumentList "-c", "src/config/mosquitto2.conf"
    }
} else {
    Write-Host "Backup Mosquitto already running."
}

Write-Host "Starting $clients_number client(s)..."

$server1 = Start-Process -PassThru -NoNewWindow -FilePath "poetry" -ArgumentList "run", "python", "src/controller/server/__init__.py", "primary", $debuggable
$server2 = Start-Process -PassThru -NoNewWindow -FilePath "poetry" -ArgumentList "run", "python", "src/controller/server/__init__.py", "secondary", $debuggable

$clients = @()

for ($i = 0; $i -lt $clients_number; $i++) {
    $port = 8080 + $i
    $client = Start-Process -PassThru -NoNewWindow -FilePath "poetry" -ArgumentList "run", "python", "src/view/__init__.py", "$port", $debuggable
    $clients += $client
    Write-Host "Started client on port $port"
}

$cleanup = {
    Write-Host "`nTerminating processes..."

    if ($mosquitto1 -and !$mosquitto1.HasExited) {
    $mosquitto1.Kill()
    }
    if ($mosquitto2 -and !$mosquitto2.HasExited) {
        $mosquitto2.Kill()
    }

    if ($server1 -and !$server1.HasExited) {
        $server1.Kill()
    }

    if ($server2 -and !$server2.HasExited) {
        $server2.Kill()
    }

    foreach ($proc in $clients) {
        if ($proc -and !$proc.HasExited) {
            $proc.Kill()
        }
    }

    Write-Host "All processes terminated."
    exit
}

$null = Register-EngineEvent PowerShell.Exiting -Action $cleanup

Write-Host "Press Ctrl+C to terminate."
while ($true) {
    Start-Sleep -Seconds 1
}
