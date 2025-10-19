@echo off
chcp 65001 >nul
title MCP Server - Interface Web API

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         MCP SERVER - INTERFACE WEB COM API REST                 ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se está no diretório correto
if not exist "api_server.py" (
    echo ❌ Erro: Arquivo api_server.py não encontrado!
    echo    Execute este script do diretório mcp-tools2
    pause
    exit /b 1
)

REM Ativar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Ambiente virtual não encontrado
    echo    Usando Python do sistema...
)

echo.
echo 📦 Verificando dependências...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ⚠️  Flask não instalado. Instalando dependências...
    pip install flask flask-cors
    if errorlevel 1 (
        echo ❌ Erro ao instalar dependências
        pause
        exit /b 1
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    INICIANDO SERVIDOR API                        ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Interface Web: http://localhost:5000
echo 📡 API REST: http://localhost:5000/api/
echo.
echo 📊 Endpoints disponíveis:
echo    GET  /api/status          - Status do servidor
echo    GET  /api/tasks           - Listar tarefas
echo    POST /api/tasks           - Criar tarefa
echo    POST /api/tasks/:id/complete - Completar tarefa
echo    DELETE /api/tasks/:id     - Deletar tarefa
echo    GET  /api/notes           - Listar notas
echo    POST /api/notes           - Criar nota
echo    GET  /api/logs            - Logs do servidor
echo.
echo ⚡ Recursos:
echo    ✓ Interface web moderna e responsiva
echo    ✓ Atualização automática a cada 5 segundos
echo    ✓ Logs em tempo real
echo    ✓ Gerenciamento completo de tarefas
echo    ✓ Visualização de estatísticas
echo.
echo 🎯 Como usar:
echo    1. Abra http://localhost:5000 no navegador
echo    2. Use a interface para gerenciar tarefas
echo    3. Veja os logs em tempo real
echo    4. As mudanças são salvas automaticamente
echo.
echo Pressione Ctrl+C para parar o servidor
echo ══════════════════════════════════════════════════════════════════
echo.

python api_server.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao iniciar servidor!
    echo.
    pause
)
