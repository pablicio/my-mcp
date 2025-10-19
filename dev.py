#!/usr/bin/env python3
"""
🛠️ Script de desenvolvimento - MCP Server Pessoal
Facilita tarefas comuns de desenvolvimento.
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    """Mostra o menu de opções."""
    print("\n" + "="*60)
    print("🛠️  MCP SERVER - FERRAMENTAS DE DESENVOLVIMENTO")
    print("="*60)
    print("\n📋 Opções disponíveis:\n")
    print("  1. 🧪 Executar testes rápidos")
    print("  2. 🔬 Executar todos os testes unitários")
    print("  3. 🧬 Executar testes de integração")
    print("  4. 📊 Executar testes com coverage")
    print("  5. 🧹 Limpar arquivos temporários")
    print("  6. 📦 Instalar/atualizar dependências")
    print("  7. 🚀 Iniciar servidor em modo debug")
    print("  8. 📝 Verificar código (lint)")
    print("  9. 🔧 Verificar configuração")
    print("  0. ❌ Sair")
    print("\n" + "="*60)

def run_command(cmd, description):
    """Executa um comando e mostra o resultado."""
    print(f"\n🔄 {description}...")
    print(f"💻 Executando: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} - Concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - Falhou com código {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Comando não encontrado: {cmd[0]}")
        return False

def quick_test():
    """Executa teste rápido."""
    return run_command(
        [sys.executable, "-m", "tests.quick_test"],
        "Teste rápido"
    )

def unit_tests():
    """Executa testes unitários."""
    return run_command(
        [sys.executable, "-m", "pytest", "tests/unit/", "-v"],
        "Testes unitários"
    )

def integration_tests():
    """Executa testes de integração."""
    return run_command(
        [sys.executable, "-m", "pytest", "tests/integration/", "-v"],
        "Testes de integração"
    )

def coverage_tests():
    """Executa testes com coverage."""
    commands = [
        ([sys.executable, "-m", "pytest", "tests/", "--cov=.", "--cov-report=html", "--cov-report=term"], 
         "Testes com coverage"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    print("\n📊 Relatório HTML gerado em: htmlcov/index.html")
    return True

def clean_project():
    """Limpa arquivos temporários."""
    print("\n🧹 Limpando arquivos temporários...")
    
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        ".pytest_cache",
        ".coverage",
        "htmlcov",
        "*.egg-info",
    ]
    
    cleaned = 0
    for pattern in patterns:
        for path in Path(".").glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    cleaned += 1
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    cleaned += 1
                print(f"   ✅ Removido: {path}")
            except Exception as e:
                print(f"   ⚠️  Erro ao remover {path}: {e}")
    
    print(f"\n✅ Limpeza concluída! {cleaned} itens removidos.")
    return True

def install_deps():
    """Instala/atualiza dependências."""
    return run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"],
        "Instalação de dependências"
    )

def start_debug():
    """Inicia servidor em modo debug."""
    import os
    os.environ["DEBUG"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    return run_command(
        [sys.executable, "main.py"],
        "Servidor em modo debug"
    )

def lint_code():
    """Verifica código (lint)."""
    print("\n📝 Verificando código...")
    
    # Verificar se flake8 está instalado
    try:
        subprocess.run([sys.executable, "-m", "flake8", "--version"], 
                      capture_output=True, check=True)
        has_flake8 = True
    except:
        has_flake8 = False
        print("⚠️  flake8 não instalado. Instale com: pip install flake8")
    
    if has_flake8:
        return run_command(
            [sys.executable, "-m", "flake8", ".", "--exclude=venv,__pycache__,.git", 
             "--max-line-length=100"],
            "Verificação de código"
        )
    else:
        print("💡 Pulando verificação de código...")
        return True

def check_config():
    """Verifica configuração."""
    print("\n🔧 Verificando configuração...\n")
    
    try:
        from config.settings import settings
        
        print("⚙️  Configurações carregadas:")
        print(f"   Host: {settings.HOST}:{settings.PORT}")
        print(f"   Debug: {settings.DEBUG}")
        print(f"   Log Level: {settings.LOG_LEVEL}")
        print(f"   Log File: {settings.LOG_FILE}")
        print(f"   Tasks DB: {settings.TASKS_DB_PATH}")
        
        dirs = settings.get_allowed_directories()
        print(f"\n📁 Diretórios permitidos: {len(dirs)}")
        if dirs:
            for d in dirs:
                exists = "✅" if Path(d).exists() else "❌"
                print(f"   {exists} {d}")
        else:
            print("   ⚠️  Nenhum diretório configurado!")
        
        print(f"\n🔐 Credenciais Google: {'✅ Configuradas' if settings.has_google_credentials else '❌ Não configuradas'}")
        
        print("\n✅ Verificação concluída!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao verificar configuração: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal."""
    options = {
        "1": ("Teste rápido", quick_test),
        "2": ("Testes unitários", unit_tests),
        "3": ("Testes de integração", integration_tests),
        "4": ("Coverage", coverage_tests),
        "5": ("Limpar projeto", clean_project),
        "6": ("Instalar dependências", install_deps),
        "7": ("Iniciar debug", start_debug),
        "8": ("Lint código", lint_code),
        "9": ("Verificar config", check_config),
    }
    
    while True:
        show_menu()
        choice = input("\n👉 Escolha uma opção: ").strip()
        
        if choice == "0":
            print("\n👋 Até logo!")
            break
        
        if choice in options:
            name, func = options[choice]
            print(f"\n{'='*60}")
            print(f"▶️  {name}")
            print("="*60)
            
            func()
            
            input("\n⏎ Pressione Enter para continuar...")
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
