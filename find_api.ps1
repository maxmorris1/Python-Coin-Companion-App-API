# API Control Script - Start and Stop the eBay Coin Scraper API
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   eBay Coin Scraper API Controller" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if API is currently running
Write-Host "Checking API status..." -ForegroundColor Yellow

$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($port8000) {
    $processId = $port8000.OwningProcess
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    
    Write-Host "✓ API server is RUNNING" -ForegroundColor Green
    Write-Host "  Process ID: $processId" -ForegroundColor White
    Write-Host "  URL: http://localhost:8000" -ForegroundColor White
    Write-Host "  Docs: http://localhost:8000/docs`n" -ForegroundColor White
    
    $choice = Read-Host "Do you want to STOP the API? (y/n)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Write-Host "Stopping API server..." -ForegroundColor Yellow
        Stop-Process -Id $processId -Force
        Start-Sleep -Seconds 1
        Write-Host "✓ API server stopped!" -ForegroundColor Green
    } else {
        Write-Host "API server remains running." -ForegroundColor Cyan
    }
} else {
    Write-Host "✗ API server is NOT running`n" -ForegroundColor Red
    
    $choice = Read-Host "Do you want to START the API? (y/n)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Write-Host "`nStarting API server..." -ForegroundColor Yellow
        Write-Host "This will open in a new window. Close the window to stop the API.`n" -ForegroundColor Cyan
        
        # Start API in a new window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python -m uvicorn api:app --reload"
        
        Start-Sleep -Seconds 2
        Write-Host "✓ API server starting!" -ForegroundColor Green
        Write-Host "  URL: http://localhost:8000" -ForegroundColor White
        Write-Host "  Docs: http://localhost:8000/docs" -ForegroundColor White
        Write-Host "`nPress Ctrl+C in the API window to stop the server." -ForegroundColor Yellow
    } else {
        Write-Host "API server remains stopped." -ForegroundColor Cyan
    }
}

Write-Host "`n========================================`n" -ForegroundColor Cyan
