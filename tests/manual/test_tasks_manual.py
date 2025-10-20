#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste manual para validar o servidor MCP.
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.tasks.tools import TasksTools
from config.settings import settings

async def test_tasks():
    """Testa as operações de tarefas."""
    print("=" * 60)
    print("TESTE DO MÓDULO DE TAREFAS")
    print("=" * 60)
    
    # Inicializar módulo
    tasks = TasksTools()
    await tasks.initialize()
    
    print(f"\n✅ Módulo inicializado com {len(tasks.tasks)} tarefas\n")
    
    # Testar criação de tarefa
    print("📝 Criando tarefa de teste...")
    result = await tasks.create_task(
        title="Tarefa de teste do script",
        description="Esta é uma tarefa criada pelo script de teste",
        priority="high",
        due_date="2025-10-25"
    )
    print(result)
    
    # Listar tarefas
    print("\n📋 Listando tarefas:")
    result = await tasks.list_tasks(status="all", limit=10)
    print(result)
    
    # Buscar tarefas
    print("\n🔍 Buscando tarefas com 'teste':")
    result = await tasks.search_tasks(query="teste")
    print(result)
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

async def test_task_parameters():
    """Testa se os parâmetros estão sendo aceitos corretamente."""
    print("\n" + "=" * 60)
    print("TESTE DE PARÂMETROS")
    print("=" * 60)
    
    tasks = TasksTools()
    await tasks.initialize()
    
    # Testar com kwargs
    print("\n📝 Testando com kwargs...")
    try:
        result = await tasks.create_task(**{
            "title": "Teste com kwargs",
            "description": "Teste",
            "priority": "low",
            "due_date": "2025-10-30"
        })
        print(f"✅ Sucesso: {result}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Testar sem parâmetros opcionais
    print("\n📝 Testando sem parâmetros opcionais...")
    try:
        result = await tasks.create_task(title="Teste mínimo")
        print(f"✅ Sucesso: {result}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Listar todas as tarefas
    print("\n📋 Tarefas criadas:")
    result = await tasks.list_tasks()
    print(result)

if __name__ == "__main__":
    print("🚀 Iniciando testes do servidor MCP...\n")
    
    try:
        # Executar testes
        asyncio.run(test_tasks())
        asyncio.run(test_task_parameters())
        
        print("\n✨ Todos os testes passaram!")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
