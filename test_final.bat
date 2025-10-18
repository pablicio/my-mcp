@echo off
echo ========================================
echo 🎉 TESTE FINAL - TODAS CORREÇÕES
echo ========================================
echo.

echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 🧹 Limpando cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul

echo.
echo ========================================
echo 🧪 TESTE 1: Settings simples
echo ========================================
python test_settings_simple.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ FALHOU! Veja o erro acima.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🧪 TESTE 2: Configuração .env
echo ========================================
python test_env.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ FALHOU! Veja o erro acima.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🧪 TESTE 3: Importações completas
echo ========================================
python test_imports.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ FALHOU! Veja o erro acima.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🧪 TESTE 4: Servidor completo
echo ========================================
python test_server.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ FALHOU! Veja o erro acima.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ TODOS OS TESTES PASSARAM!
echo ========================================
echo.
echo 🎉 Servidor MCP está pronto para uso!
echo.
echo 📋 Próximos passos:
echo    1. python main.py (iniciar servidor)
echo    2. Configurar Claude Desktop
echo    3. Reiniciar Claude Desktop
echo    4. Testar no Claude
echo.
pause
