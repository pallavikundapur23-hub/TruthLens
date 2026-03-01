#!/usr/bin/env pwsh

Write-Host "`n============================================================"
Write-Host "         TruthLens - Deepfake Detection System"
Write-Host "============================================================`n"

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Install/upgrade dependencies
Write-Host "Installing dependencies..."
pip install -q -r requirements.txt

# Run the server
Write-Host "`nStarting TruthLens Backend Server...`n"
python main.py
