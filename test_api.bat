@echo off
chcp 65001 >nul
title Teste da API REST

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              TESTE DA API REST DO MCP SERVER                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Ativar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo 🧪 Executando testes da API...
echo.

python test_api.py

echo.
pause
