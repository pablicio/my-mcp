@echo off
echo ========================================
echo 🧹 Limpando cache do Python
echo ========================================
echo.

echo 📦 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 🗑️  Removendo cache __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo 🗑️  Removendo arquivos .pyc...
del /s /q *.pyc 2>nul

echo.
echo ✅ Cache limpo!
echo.
echo 🧪 Testando importações...
python test_settings_simple.py

echo.
pause
