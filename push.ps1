# Run this script from PowerShell inside your Gravity folder
# Right-click the Gravity folder > Open in Terminal, then type: .\push.ps1

$gravityPath = "C:\Users\riobe\OneDrive\Desktop\Gravity"
$downloadsPath = "$env:USERPROFILE\Downloads\index.html"

Set-Location $gravityPath

# Check the downloaded file exists
if (-not (Test-Path $downloadsPath)) {
    Write-Host "ERROR: index.html not found in Downloads folder" -ForegroundColor Red
    Write-Host "Please download the file from Claude first, then run this script again"
    exit
}

# Get file sizes
$newSize = (Get-Item $downloadsPath).Length
$oldSize = if (Test-Path "index.html") { (Get-Item "index.html").Length } else { 0 }

Write-Host "Old index.html: $oldSize bytes"
Write-Host "New index.html: $newSize bytes"

if ($newSize -lt 100000) {
    Write-Host "ERROR: New file seems too small ($newSize bytes). Make sure you downloaded the right file." -ForegroundColor Red
    exit
}

# Copy the new file
Copy-Item $downloadsPath "index.html" -Force
Write-Host "Copied new index.html" -ForegroundColor Green

# Git push
git add index.html
git commit -m "Add pastoral photo to bio carousel"
git push origin master:main --force

Write-Host "Done! Check purposechurchofdenton.com in 30 seconds" -ForegroundColor Green
