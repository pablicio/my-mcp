@echo off
echo ========================================
echo  MCP SERVER - TODOS OS TESTES
echo ========================================
echo.

cd /d "%~dp0\.."

echo Executando TODOS os testes...
echo.

echo [1/3] Testes Unitarios...
python -m pytest tests/unit/ -v --tb=short --color=yes

echo.
echo [2/3] Testes MCP/Claude...
python -m pytest tests/mcp/ -v --tb=short --color=yes

echo.
echo [3/3] Testes de Integracao...
echo ATENCAO: Certifique-se que o servidor esta rodando!
pause
python -m pytest tests/integration/ -v --tb=short --color=yes

echo.
echo ========================================
echo  TODOS OS TESTES CONCLUIDOS
echo ========================================
pause
