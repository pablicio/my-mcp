#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar o sistema de conexões MCP
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.connection_monitor import get_connection_monitor
from modules.connections.tools import ConnectionTools


async def test_connections_module():
    """Testa o módulo de conexões."""
    print("=" * 60)
    print("TESTE: Módulo de Conexões MCP")
    print("=" * 60)
    
    # 1. Testar ConnectionMonitor
    print("\n1️⃣ Testando ConnectionMonitor...")
    monitor = get_connection_monitor()
    
    # Registrar alguns clientes de teste
    monitor.register_client("test-client-1", "Test Client 1")
    monitor.register_client("test-client-2", "Test Client 2")
    
    # Simular atividades
    monitor.record_activity("test-client-1", "list_tasks")
    monitor.record_activity("test-client-1", "create_task")
    monitor.record_activity("test-client-2", "list_notes")
    
    print("✅ Clientes registrados e atividades simuladas")
    
    # 2. Testar módulo ConnectionTools
    print("\n2️⃣ Testando ConnectionTools...")
    tools = ConnectionTools()
    
    # Verificar disponibilidade
    is_available = await tools.is_available()
    print(f"   Disponível: {is_available}")
    
    # Inicializar
    await tools.initialize()
    print(f"   Inicializado: {tools.initialized}")
    
    # Verificar ferramentas
    tool_list = tools.get_tools()
    print(f"   Ferramentas: {list(tool_list.keys())}")
    
    # 3. Testar cada ferramenta
    print("\n3️⃣ Testando ferramentas...\n")
    
    # list_connections
    print("📋 list_connections():")
    print("-" * 60)
    result = await tools.list_connections()
    print(result)
    print()
    
    # get_connection_stats
    print("📊 get_connection_stats():")
    print("-" * 60)
    result = await tools.get_connection_stats()
    print(result)
    print()
    
    # get_connection_details
    print("🔍 get_connection_details('test-client-1'):")
    print("-" * 60)
    result = await tools.get_connection_details("test-client-1")
    print(result)
    print()
    
    # 4. Verificar arquivo de dados
    print("4️⃣ Verificando arquivo de dados...")
    data_file = Path("data/mcp_connections.json")
    if data_file.exists():
        print(f"   ✅ Arquivo existe: {data_file}")
        print(f"   📦 Tamanho: {data_file.stat().st_size} bytes")
    else:
        print(f"   ❌ Arquivo não encontrado: {data_file}")
    
    # 5. Status do módulo
    print("\n5️⃣ Status do módulo:")
    status = tools.get_status()
    print(f"   {status}")
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(test_connections_module())
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
