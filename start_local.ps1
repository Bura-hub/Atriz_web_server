# Despliegue local Atriz / Swarm Lab (Windows)
# Ejecuta la API FastAPI y el frontend Vue en modo desarrollo.
# Requiere: Python 3.8+, Node.js 18+

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot

Write-Host "=== Atriz Web Server - Despliegue local ===" -ForegroundColor Cyan
Write-Host ""

# 1) API FastAPI
$ApiPath = Join-Path $ProjectRoot "swarm_lab_api"
if (-not (Test-Path $ApiPath)) {
    Write-Host "No se encuentra swarm_lab_api en $ApiPath" -ForegroundColor Red
    exit 1
}

$VenvPath = Join-Path $ApiPath "venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "[API] Creando entorno virtual en $VenvPath ..." -ForegroundColor Yellow
    python -m venv $VenvPath
}
Write-Host "[API] Activando venv e instalando dependencias..." -ForegroundColor Yellow
& (Join-Path $VenvPath "Scripts\Activate.ps1")
Set-Location $ApiPath
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[API] Iniciando Uvicorn en http://localhost:5000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ApiPath'; & '$VenvPath\Scripts\Activate.ps1'; uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload"

Start-Sleep -Seconds 3

# 2) Frontend Vue
$VuePath = Join-Path $ProjectRoot "swarm-robotics-panel"
if (-not (Test-Path $VuePath)) {
    Write-Host "No se encuentra swarm-robotics-panel en $VuePath" -ForegroundColor Red
    exit 1
}

Write-Host "[Vue] Instalando dependencias y arrancando dev server en http://localhost:8080 ..." -ForegroundColor Yellow
Set-Location $VuePath
if (-not (Test-Path "node_modules")) {
    npm install
}
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$VuePath'; npm run serve"

Write-Host ""
Write-Host "Servicios iniciados:" -ForegroundColor Green
Write-Host "  - API:       http://localhost:5000   (docs: http://localhost:5000/admin/docs)" -ForegroundColor White
Write-Host "  - Frontend:  http://localhost:8080" -ForegroundColor White
Write-Host "Cierra las ventanas de PowerShell de la API y del frontend para detenerlos." -ForegroundColor Gray
