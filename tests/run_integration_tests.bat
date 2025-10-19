@echo off
echo ========================================
echo  MCP SERVER - TESTES DE INTEGRACAO
echo ========================================
echo.

cd /d "%~dp0\.."

echo ATENCAO: Certifique-se que o servidor esta rodando!
echo Execute em outro terminal: python api_server.py
echo.
pause

echo Executando testes de integracao...
echo.

python -m pytest tests/integration/ -v --tb=short --color=yes

echo.
echo ========================================
echo  TESTES CONCLUIDOS
echo ========================================
pause
