#!/usr/bin/env python3
"""
🧪 Script de teste rápido do MCP Server
"""

import sys
import asyncio
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

async def test_server():
    """Testa os componentes principais do servidor."""
    print("="*60)
    print("🧪 TESTE DO MCP SERVER PESSOAL")
    print("="*60)
    
    errors = []
    warnings = []
    
    # Teste 1: Importações
    print("\n📦 Teste 1: Verificando importações...")
    try:
        from config.settings import settings
        from core.server import MCPPersonalServer
        from modules.filesystem.tools import FilesystemTools
        from modules.tasks.tools import TasksTools
        print("   ✅ Todas as importações OK")
    except ImportError as e:
        print(f"   ❌ Erro de importação: {e}")
        errors.append(f"Importação falhou: {e}")
        return False
    
    # Teste 2: Configurações
    print("\n⚙️  Teste 2: Verificando configurações...")
    try:
        dirs = settings.get_allowed_directories()
        print(f"   📁 Diretórios permitidos: {len(dirs)}")
        if len(dirs) == 0:
            warnings.append("Nenhum diretório permitido configurado")
            print("   ⚠️  Nenhum diretório permitido configurado em .env")
        else:
            for dir_path in dirs:
                if Path(dir_path).exists():
                    print(f"      ✅ {dir_path}")
                else:
                    print(f"      ⚠️  {dir_path} (não encontrado)")
                    warnings.append(f"Diretório não existe: {dir_path}")
        
        print(f"   🔧 Debug: {settings.DEBUG}")
        print(f"   📊 Log Level: {settings.LOG_LEVEL}")
        print(f"   🗂️  Tasks DB: {settings.TASKS_DB_PATH}")
        
    except Exception as e:
        print(f"   ❌ Erro nas configurações: {e}")
        errors.append(f"Configuração falhou: {e}")
    
    # Teste 3: Estrutura de diretórios
    print("\n📂 Teste 3: Verificando estrutura de diretórios...")
    required_dirs = ['logs', 'data']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ⚠️  {dir_name}/ (será criado)")
            dir_path.mkdir(exist_ok=True)
    
    # Teste 4: Módulos
    print("\n🔧 Teste 4: Testando módulos...")
    
    # Filesystem
    try:
        fs = FilesystemTools()
        is_available = await fs.is_available()
        print(f"   📁 Filesystem: {'✅ Disponível' if is_available else '⚠️  Não disponível'}")
        if is_available:
            await fs.initialize()
            tools = fs.get_tools()
            print(f"      Ferramentas: {len(tools)}")
    except Exception as e:
        print(f"   ❌ Filesystem erro: {e}")
        errors.append(f"Filesystem: {e}")
    
    # Tasks
    try:
        tasks = TasksTools()
        is_available = await tasks.is_available()
        print(f"   ✅ Tasks: {'✅ Disponível' if is_available else '⚠️  Não disponível'}")
        if is_available:
            await tasks.initialize()
            tools = tasks.get_tools()
            print(f"      Ferramentas: {len(tools)}")
    except Exception as e:
        print(f"   ❌ Tasks erro: {e}")
        errors.append(f"Tasks: {e}")
    
    # Teste 5: Servidor MCP
    print("\n🚀 Teste 5: Inicializando servidor...")
    try:
        server = MCPPersonalServer()
        await server.initialize()
        status = server.get_status()
        print(f"   ✅ Servidor inicializado")
        print(f"      Módulos carregados: {len(status['modules'])}")
        print(f"      Ferramentas: {status['tools_count']}")
        
        for module_name, module_status in status['modules'].items():
            print(f"      - {module_name}: {'✅' if module_status['initialized'] else '❌'}")
    except Exception as e:
        print(f"   ❌ Servidor erro: {e}")
        errors.append(f"Servidor: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    if errors:
        print(f"\n❌ Erros encontrados: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print(f"\n⚠️  Avisos: {len(warnings)}")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not errors and not warnings:
        print("\n✅ Todos os testes passaram! Servidor pronto para uso.")
        print("\n🎉 Próximos passos:")
        print("   1. Execute: python main.py")
        print("   2. Reinicie o Claude Desktop")
        print("   3. Teste no Claude: 'Liste arquivos no meu Documents'")
        return True
    elif not errors:
        print("\n⚠️  Servidor funcional mas com avisos.")
        print("   Revise os avisos acima e ajuste se necessário.")
        return True
    else:
        print("\n❌ Servidor não está pronto. Corrija os erros acima.")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_server())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Teste cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
