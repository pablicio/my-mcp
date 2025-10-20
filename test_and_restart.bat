@echo off
REM Script para testar e reiniciar o servidor MCP

echo ========================================
echo    MCP SERVER - TESTE E REINICIO
echo ========================================
echo.

:menu
echo Escolha uma opcao:
echo.
echo [1] Executar teste manual
echo [2] Limpar dados (resetar tasks.json)
echo [3] Ver logs do servidor
echo [4] Ver arquivo de tarefas
echo [5] Matar processos Python (forcar reinicio)
echo [0] Sair
echo.

set /p choice="Opcao: "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto clean
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto view
if "%choice%"=="5" goto kill
if "%choice%"=="0" goto end

echo Opcao invalida!
goto menu

:test
echo.
echo Executando testes...
python tests\manual\test_tasks_manual.py
echo.
pause
goto menu

:clean
echo.
echo Limpando dados...
echo {  > data\tasks.json
echo   "tasks": [],  >> data\tasks.json
echo   "notes": [],  >> data\tasks.json
echo   "next_task_id": 1,  >> data\tasks.json
echo   "next_note_id": 1,  >> data\tasks.json
echo   "last_updated": "2025-10-19T00:00:00.000000"  >> data\tasks.json
echo }  >> data\tasks.json
echo Dados limpos! Arquivo tasks.json resetado.
echo.
pause
goto menu

:logs
echo.
echo Ultimas 30 linhas do log:
echo ========================================
type logs\mcp_server.log | more +30
echo ========================================
echo.
pause
goto menu

:view
echo.
echo Conteudo de tasks.json:
echo ========================================
type data\tasks.json
echo ========================================
echo.
pause
goto menu

:kill
echo.
echo Matando processos Python...
taskkill /F /IM python.exe
echo Processos finalizados.
echo IMPORTANTE: Reinicie o Claude Desktop agora!
echo.
pause
goto menu

:end
echo.
echo Ate logo!
exit /b 0
