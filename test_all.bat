@echo off
echo ========================================
echo 🔧 TESTE COMPLETO DO MCP TOOLS 2
echo ========================================
echo.

echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo.

echo ========================================
echo 🧪 TESTE 1: Arquivo .env
echo ========================================
python test_env.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Teste do .env FALHOU!
    echo 💡 Leia CORRECAO_ENV.md para instruções
    echo 💡 Certifique-se que ALLOWED_DIRECTORIES use / ao invés de \
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🧪 TESTE 2: Importações
echo ========================================
python test_imports.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Teste de importações FALHOU!
    echo 💡 Execute: fix_dependencies.bat
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🧪 TESTE 3: Servidor completo
echo ========================================
python test_server.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Teste do servidor FALHOU!
    echo 💡 Verifique os logs em logs/mcp_server.log
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ TODOS OS TESTES PASSARAM!
echo ========================================
echo.
echo 🎉 Servidor está pronto para uso!
echo.
echo 📋 Próximos passos:
echo    1. python main.py (iniciar servidor)
echo    2. Reiniciar Claude Desktop
echo    3. Testar no Claude
echo.
pause
