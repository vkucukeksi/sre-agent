# Restart Service Script
param(
    [string]$ServiceName
)

Write-Host "Attempting to restart service: $ServiceName"

try {
    $service = Get-Service -Name $ServiceName -ErrorAction Stop
    Write-Host "Found service: $($service.Name)"
    
    if ($service.Status -eq "Running") {
        Write-Host "Stopping service..."
        Stop-Service -Name $ServiceName -Force
        Start-Sleep -Seconds 2
    }
    
    Write-Host "Starting service..."
    Start-Service -Name $ServiceName
    Start-Sleep -Seconds 2
    
    $updatedService = Get-Service -Name $ServiceName
    if ($updatedService.Status -eq "Running") {
        Write-Host "SUCCESS: Service $ServiceName is now running"
        exit 0
    } else {
        Write-Host "ERROR: Service $ServiceName failed to start"
        exit 1
    }
}
catch {
    Write-Host "ERROR: $_"
    exit 1
}
