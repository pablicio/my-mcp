@echo off
chcp 65001 > nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         MCP SERVER PESSOAL - MENU DE TESTE E EXECUÇÃO          ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

:menu
echo.
echo Escolha uma opção:
echo.
echo [1] 🧪 Testar Servidor (Verificar se está funcionando)
echo [2] 🚀 Iniciar Servidor (Modo Verbose com Feedback)
echo [3] 📊 Monitor em Tempo Real (NOVO!)
echo [4] 📝 Ver Logs em Tempo Real
echo [5] 🔍 Ver Status do Servidor
echo [6] 🧹 Limpar Logs
echo [7] ❌ Sair
echo.

set /p choice="Digite o número da opção: "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto start
if "%choice%"=="3" goto monitor
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto status
if "%choice%"=="6" goto clean
if "%choice%"=="7" goto end

echo Opção inválida!
goto menu

:test
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   🧪 EXECUTANDO TESTES DO SERVIDOR
echo ═══════════════════════════════════════════════════════════════
echo.
call venv\Scripts\activate.bat
python test_connection.py
echo.
echo ═══════════════════════════════════════════════════════════════
echo   Testes concluídos!
echo ═══════════════════════════════════════════════════════════════
pause
goto menu

:start
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   🚀 INICIANDO SERVIDOR MCP (Modo Verbose)
echo ═══════════════════════════════════════════════════════════════
echo.
echo   O servidor será iniciado com feedback visual.
echo   Para parar: Pressione Ctrl+C
echo.
echo   IMPORTANTE: Após iniciar, abra o Claude Desktop
echo   e teste com comandos como "liste minhas tarefas"
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
call venv\Scripts\activate.bat
python main_verbose.py
pause
goto menu

:monitor
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   📊 MONITOR EM TEMPO REAL
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Monitor visual do servidor MCP
echo   Atualiza automaticamente a cada 2 segundos
echo   Pressione Ctrl+C para voltar ao menu
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
call venv\Scripts\activate.bat
python monitor.py
goto menu

:logs
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   📝 LOGS EM TEMPO REAL
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Monitorando: logs\mcp_server.log
echo   Pressione Ctrl+C para voltar ao menu
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
if exist logs\mcp_server.log (
    powershell -Command "Get-Content 'logs\mcp_server.log' -Wait -Tail 50"
) else (
    echo   ⚠️  Arquivo de log não encontrado!
    echo   Execute o servidor primeiro.
    pause
)
goto menu

:status
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   🔍 STATUS DO SERVIDOR
echo ═══════════════════════════════════════════════════════════════
echo.

if exist logs\mcp_server.log (
    echo   📝 Últimas 20 linhas do log:
    echo   ───────────────────────────────────────────────────────────────
    echo.
    powershell -Command "Get-Content 'logs\mcp_server.log' -Tail 20"
    echo.
    echo   ───────────────────────────────────────────────────────────────
) else (
    echo   ⚠️  Nenhum log encontrado. Servidor ainda não foi iniciado.
)

echo.
if exist data\tasks.json (
    echo   📊 Banco de dados de tarefas: ✅ Existe
) else (
    echo   📊 Banco de dados de tarefas: ❌ Não existe (será criado)
)

echo.
echo ═══════════════════════════════════════════════════════════════
pause
goto menu

:clean
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   🧹 LIMPEZA DE LOGS
echo ═══════════════════════════════════════════════════════════════
echo.

if exist logs\mcp_server.log (
    del logs\mcp_server.log
    echo   ✅ Log principal deletado
) else (
    echo   ℹ️  Nenhum log encontrado
)

if exist logs\mcp_server.log.1 (
    del logs\mcp_server.log.*
    echo   ✅ Logs rotativos deletados
)

echo.
echo   Limpeza concluída!
echo.
echo ═══════════════════════════════════════════════════════════════
pause
goto menu

:end
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo   👋 Até logo!
echo ═══════════════════════════════════════════════════════════════
echo.
exit /b
