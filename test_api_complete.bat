@echo off
chcp 65001 >nul
cls

echo ============================================================
echo 🧪 MCP SERVER - TESTE AUTOMATIZADO DA API
echo ============================================================
echo.

REM Ativar ambiente virtual
if exist venv\Scripts\activate.bat (
    echo 📦 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Ambiente virtual não encontrado
    echo    Execute setup.py primeiro
    pause
    exit /b 1
)

echo.
echo 🔧 Instalando dependências de teste...
pip install requests colorama -q

echo.
echo 🚀 Executando testes...
echo.

python test_api_complete.py

echo.
echo ============================================================
echo.
pause
