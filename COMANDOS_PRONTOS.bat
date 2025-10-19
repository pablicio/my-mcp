@echo off
REM 🚀 Comandos úteis para o MCP Server

:menu
cls
echo ============================================================
echo   MCP SERVER PESSOAL - COMANDOS UTEIS
echo ============================================================
echo.
echo   1. Iniciar servidor
echo   2. Teste rapido
echo   3. Testes unitarios
echo   4. Menu de desenvolvimento
echo   5. Limpar projeto
echo   6. Instalar dependencias
echo   7. Ver logs
echo   0. Sair
echo.
echo ============================================================
set /p choice="Escolha uma opcao: "

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto quick_test
if "%choice%"=="3" goto unit_tests
if "%choice%"=="4" goto dev_menu
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto install
if "%choice%"=="7" goto logs
if "%choice%"=="0" goto end

echo.
echo Opcao invalida!
timeout /t 2 >nul
goto menu

:start_server
echo.
echo Iniciando servidor...
python main.py
pause
goto menu

:quick_test
echo.
echo Executando teste rapido...
python -m tests.quick_test
pause
goto menu

:unit_tests
echo.
echo Executando testes unitarios...
python -m pytest tests/unit/ -v
pause
goto menu

:dev_menu
echo.
python dev.py
goto menu

:clean
echo.
echo Limpando projeto...
python clean_project.py
pause
goto menu

:install
echo.
echo Instalando dependencias...
pip install -r requirements.txt
pause
goto menu

:logs
echo.
echo Mostrando ultimas linhas do log...
powershell -command "Get-Content logs\mcp_server.log -Tail 50"
pause
goto menu

:end
echo.
echo Ate logo!
exit /b 0
