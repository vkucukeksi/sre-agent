param(
    [string]$ServiceName
)

Write-Host "Simulating restart of service: $ServiceName"

Start-Sleep -Seconds 2

Write-Host "Stopping service..."
Start-Sleep -Seconds 1

Write-Host "Starting service..."
Start-Sleep -Seconds 1

Write-Host "SUCCESS: Service $ServiceName restarted successfully"

exit 0