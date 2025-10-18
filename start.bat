@echo off
REM Script para iniciar o MCP Server no Windows

echo ========================================
echo   MCP Server Pessoal - Inicializacao
echo ========================================
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.9+ de python.org
    pause
    exit /b 1
)

REM Verificar se está no diretório correto
if not exist "main.py" (
    echo ERRO: main.py nao encontrado!
    echo Execute este script no diretorio do projeto
    pause
    exit /b 1
)

REM Verificar se .env existe
if not exist ".env" (
    echo AVISO: Arquivo .env nao encontrado
    echo Execute: python setup.py
    echo.
    set /p continue="Continuar mesmo assim? (S/N): "
    if /i not "%continue%"=="S" exit /b 1
)

echo Iniciando servidor MCP...
echo.
echo Para parar: Ctrl+C
echo Logs: logs\mcp_server.log
echo.

REM Iniciar o servidor
python main.py

pause
