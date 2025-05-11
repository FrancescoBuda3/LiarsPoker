param (
    [int]$clients_number
)

if (-not $clients_number) {
    Write-Host "Usage: .\start_clients.ps1 <clients_number>"
    exit 1
}

$mosquittoRunning = Get-Process -Name "mosquitto" -ErrorAction SilentlyContinue

if (-not $mosquittoRunning) {
    Write-Host "Mosquitto is not running. Starting it..."
    $mosquitto = Start-Process -PassThru -WindowStyle Hidden -FilePath "mosquitto" 
} else {
    Write-Host "Mosquitto is already running."
}

Write-Host "Starting $clients_number client(s)..."

$server = Start-Process -PassThru -NoNewWindow -FilePath "poetry" -ArgumentList "run", "python", "src/controller/server/__init__.py"

$clients = @()

for ($i = 0; $i -lt $clients_number; $i++) {
    $port = 8080 + $i
    $client = Start-Process -PassThru -NoNewWindow -FilePath "poetry" -ArgumentList "run", "python", "src/view/__init__.py", "$port"
    $clients += $client
    Write-Host "Started client on port $port"
}

$cleanup = {
    Write-Host "`nTerminating processes..."

    if ($server -and !$server.HasExited) {
        $server.Kill()
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
