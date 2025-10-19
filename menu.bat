@echo off
chcp 65001 >nul
title MCP Server - Menu Principal

:MENU
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              MCP SERVER - MENU PRINCIPAL                         ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo  Escolha uma opção:
echo.
echo  [1] 🌐 Iniciar Interface Web          (Recomendado para uso visual)
echo  [2] 🤖 Iniciar MCP Server             (Para Claude Desktop)
echo  [3] 🧪 Testar API                     (Verificar se está funcionando)
echo  [4] 📊 Ver Status                     (Informações do servidor)
echo  [5] 📝 Ver Logs                       (Últimos eventos)
echo  [6] 🧹 Limpar Dados                   (Reset de tarefas e notas)
echo  [7] 📚 Abrir Documentação             (Guias e manuais)
echo  [8] ❌ Sair
echo.
set /p opcao="Digite o número da opção: "

if "%opcao%"=="1" goto INTERFACE_WEB
if "%opcao%"=="2" goto MCP_SERVER
if "%opcao%"=="3" goto TESTAR_API
if "%opcao%"=="4" goto STATUS
if "%opcao%"=="5" goto LOGS
if "%opcao%"=="6" goto LIMPAR
if "%opcao%"=="7" goto DOCS
if "%opcao%"=="8" goto SAIR

echo.
echo ❌ Opção inválida!
timeout /t 2 >nul
goto MENU

:INTERFACE_WEB
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    INTERFACE WEB                                 ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Iniciando servidor da interface web...
echo.
call start_web_interface.bat
goto MENU

:MCP_SERVER
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    MCP SERVER                                    ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🤖 Iniciando MCP Server para Claude Desktop...
echo.
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)
python main.py
pause
goto MENU

:TESTAR_API
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    TESTE DA API                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🧪 Executando suite de testes...
echo.
echo ⚠️  Certifique-se de que o servidor está rodando!
echo    Se não estiver, abra outro terminal e execute a opção [1]
echo.
pause
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)
python test_api.py
echo.
pause
goto MENU

:STATUS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    STATUS DO SISTEMA                             ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se ambiente virtual existe
if exist "venv\Scripts\python.exe" (
    echo ✅ Ambiente virtual: OK
) else (
    echo ❌ Ambiente virtual: NÃO ENCONTRADO
)

REM Verificar arquivos principais
if exist "api_server.py" (
    echo ✅ API Server: OK
) else (
    echo ❌ API Server: NÃO ENCONTRADO
)

if exist "main.py" (
    echo ✅ MCP Server: OK
) else (
    echo ❌ MCP Server: NÃO ENCONTRADO
)

if exist "index.html" (
    echo ✅ Interface Web: OK
) else (
    echo ❌ Interface Web: NÃO ENCONTRADA
)

REM Verificar dados
if exist "data\tasks.json" (
    echo ✅ Banco de dados: OK
    echo.
    echo 📊 Conteúdo do banco de dados:
    type data\tasks.json
) else (
    echo ❌ Banco de dados: NÃO ENCONTRADO
)

echo.
echo 📁 Estrutura de diretórios:
if exist "data" echo    ✅ data/
if exist "logs" echo    ✅ logs/
if exist "modules" echo    ✅ modules/
if exist "config" echo    ✅ config/
if exist "venv" echo    ✅ venv/

echo.
pause
goto MENU

:LOGS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    LOGS DO SERVIDOR                              ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

if exist "logs\mcp_server.log" (
    echo 📊 Últimas 30 linhas do log:
    echo.
    echo ────────────────────────────────────────────────────────────────
    powershell -Command "Get-Content logs\mcp_server.log -Tail 30"
    echo ────────────────────────────────────────────────────────────────
) else (
    echo ❌ Arquivo de log não encontrado
    echo.
    echo Execute o servidor pelo menos uma vez para gerar logs.
)

echo.
pause
goto MENU

:LIMPAR
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    LIMPAR DADOS                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ATENÇÃO: Esta ação vai deletar TODAS as tarefas e notas!
echo.
set /p confirma="Tem certeza? (S/N): "

if /i "%confirma%"=="S" (
    echo.
    echo 🧹 Limpando dados...
    
    REM Criar backup antes
    if exist "data\tasks.json" (
        copy "data\tasks.json" "data\tasks.json.backup" >nul 2>&1
        echo ✅ Backup criado: data\tasks.json.backup
    )
    
    REM Criar novo arquivo vazio
    echo {"tasks": [], "notes": [], "last_updated": ""} > data\tasks.json
    echo ✅ Dados limpos!
    echo.
    echo 💡 Se precisar restaurar, renomeie tasks.json.backup para tasks.json
) else (
    echo.
    echo ❌ Operação cancelada
)

echo.
pause
goto MENU

:DOCS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    DOCUMENTAÇÃO                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 📚 Documentação disponível:
echo.
echo  [1] QUICKSTART_WEB.md      - Início rápido da interface web
echo  [2] WEB_INTERFACE.md       - Documentação completa da interface
echo  [3] SETUP_COMPLETO.md      - Guia de setup e implementação
echo  [4] README.md              - Visão geral do projeto
echo  [5] QUICKSTART_VISUAL.md   - Guia visual do MCP Server
echo  [6] Voltar ao menu
echo.
set /p doc="Escolha o documento (1-6): "

if "%doc%"=="1" start QUICKSTART_WEB.md
if "%doc%"=="2" start WEB_INTERFACE.md
if "%doc%"=="3" start SETUP_COMPLETO.md
if "%doc%"=="4" start README.md
if "%doc%"=="5" start QUICKSTART_VISUAL.md
if "%doc%"=="6" goto MENU

echo.
echo Abrindo documento...
timeout /t 2 >nul
goto MENU

:SAIR
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    ATÉ LOGO!                                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 👋 Obrigado por usar o MCP Server!
echo.
echo 💡 Dicas rápidas:
echo    - Interface web: start_web_interface.bat
echo    - MCP Server: python main.py
echo    - Testes: test_api.bat
echo.
timeout /t 3
exit
