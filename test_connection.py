#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a comunicação MCP.
Simula requisições do Claude Desktop para validar o servidor.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.server import MCPPersonalServer
from config.settings import settings
from config.logging import setup_logging

async def test_server_initialization():
    """Testa inicialização do servidor."""
    print("\n" + "="*70)
    print("🧪 TESTE 1: Inicialização do Servidor")
    print("="*70)
    
    try:
        server = MCPPersonalServer()
        await server.initialize()
        
        print(f"✅ Servidor inicializado com sucesso!")
        print(f"   Módulos carregados: {len(server.modules)}")
        print(f"   Ferramentas registradas: {len(server.registry.tools)}")
        
        return server, True
    except Exception as e:
        print(f"❌ Falha na inicialização: {e}")
        return None, False

async def test_modules(server):
    """Testa cada módulo individualmente."""
    print("\n" + "="*70)
    print("🧪 TESTE 2: Verificação de Módulos")
    print("="*70)
    
    results = {}
    for name, module in server.modules.items():
        try:
            status = module.get_status()
            available = await module.is_available()
            
            print(f"\n📦 Módulo: {name.upper()}")
            print(f"   Status: {status.get('status', 'unknown')}")
            print(f"   Disponível: {'✅ Sim' if available else '❌ Não'}")
            
            results[name] = available
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            results[name] = False
    
    return results

async def test_tasks_module(server):
    """Testa operações do módulo de tarefas."""
    print("\n" + "="*70)
    print("🧪 TESTE 3: Módulo de Tarefas")
    print("="*70)
    
    if 'tasks' not in server.modules:
        print("❌ Módulo de tarefas não está carregado")
        return False
    
    tasks_module = server.modules['tasks']
    
    try:
        # Criar uma tarefa de teste
        print("\n📝 Criando tarefa de teste...")
        result = await tasks_module.create_task(
            title="Tarefa de Teste",
            description="Esta é uma tarefa de teste",
            priority="medium"
        )
        print(f"✅ {result}")
        
        # Listar tarefas
        print("\n📋 Listando tarefas...")
        result = await tasks_module.list_tasks()
        print(f"✅ {result}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de tarefas: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_filesystem_module(server):
    """Testa operações do módulo de filesystem."""
    print("\n" + "="*70)
    print("🧪 TESTE 4: Módulo de Filesystem")
    print("="*70)
    
    if 'filesystem' not in server.modules:
        print("❌ Módulo de filesystem não está carregado")
        return False
    
    fs_module = server.modules['filesystem']
    
    try:
        # Listar diretórios permitidos
        print("\n📁 Diretórios permitidos:")
        allowed_dirs = settings.get_allowed_directories()
        for i, dir_path in enumerate(allowed_dirs, 1):
            print(f"   {i}. {dir_path}")
        
        if allowed_dirs:
            # Tentar listar o primeiro diretório
            test_dir = allowed_dirs[0]
            print(f"\n📂 Listando conteúdo de: {test_dir}")
            result = await fs_module.list_directory(test_dir)
            print(f"✅ {result[:200]}...")  # Primeiros 200 caracteres
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de filesystem: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_tool_registration(server):
    """Verifica se as ferramentas estão corretamente registradas."""
    print("\n" + "="*70)
    print("🧪 TESTE 5: Registro de Ferramentas")
    print("="*70)
    
    print(f"\n🔧 Ferramentas registradas ({len(server.registry.tools)}):")
    for i, tool_name in enumerate(server.registry.tools.keys(), 1):
        print(f"   {i}. {tool_name}")
    
    return len(server.registry.tools) > 0

async def main():
    """Executa todos os testes."""
    setup_logging()
    
    print("\n" + "🧪 INICIANDO TESTES DO MCP SERVER" + "\n")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Debug: {settings.DEBUG}")
    print(f"📝 Log: {settings.LOG_FILE}")
    
    results = {}
    
    # Teste 1: Inicialização
    server, success = await test_server_initialization()
    results['initialization'] = success
    
    if not success:
        print("\n❌ Falha crítica na inicialização. Abortando testes.")
        return
    
    # Teste 2: Módulos
    module_results = await test_modules(server)
    results['modules'] = module_results
    
    # Teste 3: Tarefas
    results['tasks'] = await test_tasks_module(server)
    
    # Teste 4: Filesystem
    results['filesystem'] = await test_filesystem_module(server)
    
    # Teste 5: Registro de ferramentas
    results['tools'] = await test_tool_registration(server)
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test.upper():<20} {status}")
    
    print(f"\n{'✅' if passed == total else '⚠️'} Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Execute: python main_verbose.py")
        print("   2. Abra o Claude Desktop")
        print("   3. Teste com: 'liste minhas tarefas'")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("   Verifique os erros acima e o arquivo de log")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Testes interrompidos")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
