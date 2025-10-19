@echo off
REM 🚀 Script para iniciar o MCP Server no Windows

echo ============================================================
echo   MCP Server Pessoal v1.0.0
echo ============================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python nao encontrado!
    echo 💡 Instale Python 3.9+ de python.org
    pause
    exit /b 1
)

REM Verificar diretório
if not exist "main.py" (
    echo ❌ ERRO: main.py nao encontrado!
    echo 💡 Execute no diretorio do projeto
    pause
    exit /b 1
)

REM Verificar .env
if not exist ".env" (
    echo ⚠️  AVISO: Arquivo .env nao encontrado
    echo 💡 Execute primeiro: python setup.py
    echo.
    set /p continue="Continuar mesmo assim? (S/N): "
    if /i not "%continue%"=="S" exit /b 1
)

echo ✅ Iniciando servidor MCP...
echo.
echo 🔧 Para parar: Ctrl+C
echo 📊 Logs: logs\mcp_server.log
echo 💡 Depois de iniciar, reinicie o Claude Desktop
echo.
echo ============================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ❌ Servidor encerrou com erro
    echo 💡 Verifique os logs em: logs\mcp_server.log
    pause
)
