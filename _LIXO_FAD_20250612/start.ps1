# Script para iniciar o servidor FastAPI do FAD-GEO
Write-Host "Iniciando FAD-GEO..." -ForegroundColor Green

# Verificar se o ambiente virtual existe
$venvPath = "$PSScriptRoot\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host "Erro: Ambiente virtual não encontrado em $venvPath" -ForegroundColor Red
    Write-Host "Execute primeiro: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Ativar o ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
& $venvPath

# Verificar se o main.py existe
if (-not (Test-Path "$PSScriptRoot\main.py")) {
    Write-Host "Erro: main.py não encontrado!" -ForegroundColor Red
    exit 1
}

# Rodar o servidor FastAPI com Uvicorn
Write-Host "Iniciando servidor FastAPI em http://127.0.0.1:8000" -ForegroundColor Green
uvicorn main:app --reload --host 127.0.0.1 --port 8000
