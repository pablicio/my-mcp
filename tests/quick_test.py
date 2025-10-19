#!/usr/bin/env python3
"""
🧪 Teste Rápido - MCP Server Pessoal
Valida configuração básica e módulos principais.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Testa se todas as importações funcionam."""
    print("📦 Testando importações...")
    try:
        from config.settings import settings
        from core.server import MCPPersonalServer
        from modules.filesystem.tools import FilesystemTools
        from modules.tasks.tools import TasksTools
        print("✅ Todas as importações OK")
        return True
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False

def test_settings():
    """Testa se as configurações estão corretas."""
    print("\n⚙️ Testando configurações...")
    try:
        from config.settings import settings
        
        print(f"   Host: {settings.HOST}")
        print(f"   Port: {settings.PORT}")
        print(f"   Debug: {settings.DEBUG}")
        print(f"   Log Level: {settings.LOG_LEVEL}")
        
        allowed_dirs = settings.get_allowed_directories()
        print(f"   Diretórios permitidos: {len(allowed_dirs)}")
        for d in allowed_dirs:
            print(f"      - {d}")
        
        if not allowed_dirs:
            print("⚠️ Nenhum diretório permitido configurado!")
            print("   Configure ALLOWED_DIRECTORIES no arquivo .env")
        
        print("✅ Configurações OK")
        return True
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False

def test_modules():
    """Testa disponibilidade dos módulos."""
    print("\n🔧 Testando módulos...")
    try:
        import asyncio
        from modules.filesystem.tools import FilesystemTools
        from modules.tasks.tools import TasksTools
        
        async def check_modules():
            results = {}
            
            # Filesystem
            fs = FilesystemTools()
            results['filesystem'] = await fs.is_available()
            
            # Tasks
            tasks = TasksTools()
            results['tasks'] = await tasks.is_available()
            
            return results
        
        results = asyncio.run(check_modules())
        
        for module, available in results.items():
            status = "✅" if available else "❌"
            print(f"   {status} {module}: {'disponível' if available else 'indisponível'}")
        
        all_ok = all(results.values())
        if all_ok:
            print("✅ Todos os módulos OK")
        else:
            print("⚠️ Alguns módulos não estão disponíveis")
        
        return all_ok
    except Exception as e:
        print(f"❌ Erro ao testar módulos: {e}")
        return False

def test_server_init():
    """Testa inicialização do servidor."""
    print("\n🚀 Testando servidor...")
    try:
        import asyncio
        from core.server import MCPPersonalServer
        
        async def init_server():
            server = MCPPersonalServer()
            await server.initialize()
            status = server.get_status()
            return status
        
        status = asyncio.run(init_server())
        
        print(f"   Status: {status['status']}")
        print(f"   Módulos carregados: {len(status['modules'])}")
        print(f"   Ferramentas: {status['tools_count']}")
        
        for module_name, module_status in status['modules'].items():
            init_status = "✅" if module_status['initialized'] else "❌"
            print(f"      {init_status} {module_name}")
        
        print("✅ Servidor OK")
        return True
    except Exception as e:
        print(f"❌ Erro ao testar servidor: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes."""
    print("="*60)
    print("🧪 TESTE RÁPIDO - MCP SERVER PESSOAL")
    print("="*60)
    
    results = {
        "Importações": test_imports(),
        "Configurações": test_settings(),
        "Módulos": test_modules(),
        "Servidor": test_server_init()
    }
    
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\n💡 Próximos passos:")
        print("   1. Execute: python main.py")
        print("   2. Reinicie o Claude Desktop")
        print("   3. Teste no Claude: 'Liste arquivos em Documents'")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("\n💡 Verifique:")
        print("   1. Arquivo .env está configurado?")
        print("   2. Dependências instaladas? pip install -r requirements.txt")
        print("   3. Python 3.9+? python --version")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
