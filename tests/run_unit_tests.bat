@echo off
echo ========================================
echo  MCP SERVER - TESTES UNITARIOS
echo ========================================
echo.

cd /d "%~dp0"

echo Executando testes unitarios...
echo.

python -m pytest tests/unit/ -v --tb=short --color=yes

echo.
echo ========================================
echo  TESTES CONCLUIDOS
echo ========================================
pause
