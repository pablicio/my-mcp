:: ===================================
:: 🚀 COMANDOS PRONTOS - Cole no CMD
:: ===================================

:: Navegue até a pasta do projeto primeiro
cd C:\projetos\IA\mcp\mcp-tools2

:: Execute o script de correção
fix_dependencies.bat

:: ===================================
:: OU execute os comandos individuais:
:: ===================================

:: 1. Ativar ambiente virtual
call venv\Scripts\activate.bat

:: 2. Desinstalar pacotes antigos
pip uninstall -y pydantic pydantic-settings

:: 3. Instalar dependências corretas
pip install --upgrade pip
pip install -r requirements.txt

:: 4. Testar importações
python test_imports.py

:: 5. Teste completo
python test_server.py

:: 6. Iniciar servidor (se testes passarem)
python main.py

:: ===================================
:: 💡 DICA: Cole TUDO de uma vez!
:: ===================================
