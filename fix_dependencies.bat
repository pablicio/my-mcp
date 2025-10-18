@echo off
echo ========================================
echo 🔧 Corrigindo dependências do MCP Tools
echo ========================================
echo.

echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 🗑️  Desinstalando pacotes problemáticos...
pip uninstall -y pydantic pydantic-settings

echo.
echo 📥 Instalando dependências atualizadas...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Dependências corrigidas!
echo.
echo 🧪 Executando teste...
python test_server.py

echo.
echo ========================================
echo Correção concluída!
echo ========================================
pause
