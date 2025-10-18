#!/usr/bin/env python3
"""
🚀 Setup automatizado do MCP Server Pessoal
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime cabeçalho formatado."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(number, text):
    """Imprime passo formatado."""
    print(f"\n{'🔹'} Passo {number}: {text}")
    print("-" * 50)

def check_python_version():
    """Verifica versão do Python."""
    version = sys.version_info
    if version < (3, 9):
        print("❌ Python 3.9+ é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def install_dependencies():
    """Instala dependências do projeto."""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
        ])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_env_file():
    """Cria arquivo .env se não existir."""
    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("⚠️  Arquivo .env já existe")
        response = input("   Deseja sobrescrever? (s/N): ").lower()
        if response != 's':
            print("   Mantendo .env existente")
            return

    if not env_example.exists():
        print("❌ Arquivo .env.example não encontrado!")
        return

    # Copiar .env.example para .env
    with open(env_example, 'r', encoding='utf-8') as f:
        content = f.read()

    # Obter diretórios padrão baseado no sistema operacional
    home = Path.home()
    if platform.system() == "Windows":
        default_dirs = f"{home}\\Documents,{home}\\Desktop"
    else:
        default_dirs = f"{home}/Documents,{home}/Desktop"

    # Solicitar diretórios permitidos
    print("\n📁 Configuração de diretórios permitidos:")
    print("   Informe os caminhos absolutos separados por vírgula")
    print(f"   Exemplo: {default_dirs}")
    user_dirs = input(f"   Diretórios (Enter para padrão): ").strip()
    
    if not user_dirs:
        user_dirs = default_dirs
        print(f"   Usando: {user_dirs}")

    # Atualizar conteúdo
    content = content.replace(
        "ALLOWED_DIRECTORIES=/home/usuario/Documents,/home/usuario/Desktop",
        f"ALLOWED_DIRECTORIES={user_dirs}"
    )

    # Salvar .env
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Arquivo .env criado com sucesso")

def get_claude_config_path():
    """Retorna o caminho do arquivo de configuração do Claude Desktop."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows":
        return Path(os.getenv('APPDATA')) / "Claude/claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config/Claude/claude_desktop_config.json"

def configure_claude_desktop():
    """Configura o Claude Desktop para usar este servidor MCP."""
    print("\n🔧 Configurando Claude Desktop...")
    
    config_path = get_claude_config_path()
    project_path = Path.cwd().resolve()
    main_py = project_path / "main.py"

    if not main_py.exists():
        print("❌ Arquivo main.py não encontrado!")
        return False

    # Criar diretório se não existir
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Ler configuração existente ou criar nova
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {"mcpServers": {}}

    # Adicionar/atualizar configuração do servidor
    config["mcpServers"]["personal-server"] = {
        "command": sys.executable,
        "args": [str(main_py)],
        "env": {
            "PYTHONPATH": str(project_path)
        }
    }

    # Salvar configuração
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Claude Desktop configurado")
    print(f"   Config: {config_path}")
    print(f"   Servidor: {main_py}")
    
    return True

def create_directories():
    """Cria diretórios necessários."""
    print("\n📂 Criando estrutura de diretórios...")
    
    dirs = ["logs", "data", "tests"]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")

def test_installation():
    """Testa a instalação."""
    print("\n🧪 Testando instalação...")
    
    try:
        # Tentar importar módulos principais
        sys.path.insert(0, str(Path.cwd()))
        
        from config.settings import settings
        from core.server import MCPPersonalServer
        
        print("✅ Importações bem-sucedidas")
        print(f"   Diretórios permitidos: {len(settings.ALLOWED_DIRECTORIES)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def print_next_steps():
    """Imprime próximos passos."""
    print("\n" + "="*60)
    print("  ✨ Setup concluído com sucesso!")
    print("="*60)
    
    print("\n📋 Próximos passos:\n")
    print("1. Revisar configurações em .env")
    print("2. Iniciar o servidor: python main.py")
    print("3. Reiniciar o Claude Desktop")
    print("4. Testar no Claude: 'Liste arquivos no meu Documents'")
    
    print("\n📚 Documentação:")
    print("   - README.md: Guia completo")
    print("   - index.html: Interface web (abrir no navegador)")
    
    print("\n💡 Dicas:")
    print("   - Logs: ./logs/mcp_server.log")
    print("   - Config Claude: Use 'python setup.py' para reconfigurar")
    print("   - Problemas? Veja README.md seção Troubleshooting")
    
    print("\n" + "="*60 + "\n")

def main():
    """Função principal do setup."""
    print_header("🚀 Setup do MCP Server Pessoal v1.0.0")
    
    # Passo 1: Verificar Python
    print_step(1, "Verificando versão do Python")
    check_python_version()
    
    # Passo 2: Criar diretórios
    print_step(2, "Criando estrutura de diretórios")
    create_directories()
    
    # Passo 3: Instalar dependências
    print_step(3, "Instalando dependências")
    if not install_dependencies():
        print("\n❌ Setup falhou na instalação de dependências")
        sys.exit(1)
    
    # Passo 4: Criar .env
    print_step(4, "Configurando arquivo .env")
    create_env_file()
    
    # Passo 5: Configurar Claude Desktop
    print_step(5, "Configurando Claude Desktop")
    configure_claude_desktop()
    
    # Passo 6: Testar instalação
    print_step(6, "Testando instalação")
    if not test_installation():
        print("\n⚠️  Alguns testes falharam, mas o setup está completo")
    
    # Próximos passos
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
