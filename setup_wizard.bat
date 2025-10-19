@echo off
chcp 65001 > nul
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║          🎉 MCP SERVER PESSOAL - GUIA DE PRIMEIROS PASSOS 🎉         ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo.
echo  Este guia vai te ajudar a configurar e testar o servidor MCP!
echo  Siga os passos abaixo em ordem.
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.
pause
cls

:step1
color 0B
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║  PASSO 1/5: Verificar Ambiente Virtual                                ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo  Verificando se o ambiente virtual existe...
echo.

if exist "venv\Scripts\activate.bat" (
    echo  ✅ Ambiente virtual encontrado!
    echo.
    echo  Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    echo.
    echo  ✅ Ambiente virtual ativado!
) else (
    echo  ❌ Ambiente virtual NÃO encontrado!
    echo.
    echo  Por favor, crie o ambiente virtual primeiro:
    echo     python -m venv venv
    echo     venv\Scripts\activate
    echo     pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════════════
pause

:step2
color 0E
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║  PASSO 2/5: Verificar Arquivo .env                                    ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo  Verificando configurações...
echo.

if exist ".env" (
    echo  ✅ Arquivo .env encontrado!
    echo.
    echo  Conteúdo atual:
    echo  ───────────────────────────────────────────────────────────────────
    type .env
    echo  ───────────────────────────────────────────────────────────────────
) else (
    echo  ❌ Arquivo .env NÃO encontrado!
    echo.
    echo  Criando arquivo .env a partir do exemplo...
    if exist ".env.example" (
        copy .env.example .env > nul
        echo  ✅ Arquivo .env criado!
    ) else (
        echo  ❌ Arquivo .env.example também não existe!
    )
)

echo.
echo ════════════════════════════════════════════════════════════════════════
pause

:step3
color 0D
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║  PASSO 3/5: Executar Testes Automáticos                               ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo  Executando bateria de testes...
echo  Isso pode levar alguns segundos.
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.

python test_connection.py

echo.
echo ════════════════════════════════════════════════════════════════════════
echo.
echo  Os testes terminaram!
echo.
set /p tests_ok="Todos os testes passaram? (s/n): "

if /i "%tests_ok%"=="n" (
    echo.
    echo  ❌ Alguns testes falharam!
    echo.
    echo  Por favor, verifique os erros acima e corrija antes de continuar.
    echo  Você pode:
    echo     1. Verificar o arquivo .env
    echo     2. Verificar as dependências: pip install -r requirements.txt
    echo     3. Ver os logs: type logs\mcp_server.log
    echo.
    pause
    exit /b 1
)

echo.
echo  ✅ Ótimo! Vamos continuar...
echo.
pause

:step4
color 0A
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║  PASSO 4/5: Iniciar Servidor MCP                                      ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo  Agora vamos iniciar o servidor em modo verbose.
echo  Você verá todas as informações de inicialização.
echo.
echo  📝 IMPORTANTE:
echo     - O servidor vai ficar rodando (não fecha o terminal!)
echo     - Você verá o feedback de inicialização
echo     - Depois, abra o Claude Desktop para testar
echo.
echo  Pressione qualquer tecla para iniciar o servidor...
pause > nul
cls

python main_verbose.py

pause

:step5
color 0B
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║  PASSO 5/5: Testar com Claude Desktop                                 ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo  Servidor foi iniciado e parado.
echo.
echo  📋 CHECKLIST DE TESTE COM CLAUDE:
echo.
echo  [ ] 1. Reinicie o servidor: run_tests.bat ^>^> [2]
echo  [ ] 2. Abra o Claude Desktop
echo  [ ] 3. Digite: "liste minhas tarefas"
echo  [ ] 4. Digite: "crie uma tarefa: Testar MCP Server"
echo  [ ] 5. Digite: "liste minhas tarefas" novamente
echo.
echo  Se funcionar, você verá suas tarefas!
echo.
echo  💡 DICA: Para monitorar atividade em tempo real:
echo     - Abra outro terminal
echo     - Execute: run_tests.bat ^>^> [3]
echo     - Deixe aberto enquanto usa o Claude
echo.
echo ════════════════════════════════════════════════════════════════════════
echo.
pause

:final
color 0A
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║                  🎉 CONFIGURAÇÃO COMPLETA! 🎉                         ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo.
echo  ✅ Seu MCP Server está configurado e testado!
echo.
echo  📚 PRÓXIMOS PASSOS:
echo.
echo     1. Use o menu principal:
echo        ^>^> run_tests.bat
echo.
echo     2. Leia a documentação:
echo        - README.md              (Visão geral)
echo        - QUICKSTART_VISUAL.md   (Guia rápido)
echo        - GUIA_TESTES.md        (Como testar)
echo        - MELHORIAS.md          (O que foi feito)
echo.
echo     3. Comandos úteis no Claude:
echo        "liste minhas tarefas"
echo        "crie uma tarefa: [descrição]"
echo        "crie uma nota sobre [assunto]"
echo        "liste arquivos em [diretório]"
echo.
echo.
echo  🚀 INICIAR AGORA:
echo.
set /p start_menu="Deseja abrir o menu principal? (s/n): "

if /i "%start_menu%"=="s" (
    cls
    call run_tests.bat
) else (
    echo.
    echo  Ok! Execute 'run_tests.bat' quando quiser começar.
    echo.
)

echo.
echo ════════════════════════════════════════════════════════════════════════
echo.
pause
