#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico e Correção do Problema de Sincronização de Tarefas

Problema:
- Tarefas criadas via Claude (MCP) não aparecem na interface web
- Interface web mostra dados desatualizados

Causa:
- Duas instâncias separadas do TasksModule (MCP Server e API Server)
- Ambas lêem/escrevem no mesmo arquivo, mas têm caches em memória

Solução:
1. Verificar se o arquivo está sendo atualizado
2. Forçar reload dos dados no API Server
3. Adicionar polling mais frequente ou webhook
"""

import json
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from modules.tasks.tools import TasksTools
from config.settings import settings


async def diagnostico():
    """Diagnóstico completo do sistema de tarefas"""
    print("="*70)
    print("🔍 DIAGNÓSTICO: Sistema de Tarefas")
    print("="*70)
    print()
    
    # 1. Verificar arquivo JSON
    json_path = Path(settings.TASKS_DB_PATH)
    print(f"📂 Arquivo de dados: {json_path}")
    print(f"   Existe: {json_path.exists()}")
    
    if json_path.exists():
        print(f"   Tamanho: {json_path.stat().st_size} bytes")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"   Tarefas no arquivo: {len(data.get('tasks', []))}")
        print(f"   Notas no arquivo: {len(data.get('notes', []))}")
        print(f"   Última atualização: {data.get('last_updated', 'N/A')}")
    print()
    
    # 2. Inicializar módulo e verificar
    print("🔧 Inicializando módulo de tarefas...")
    tasks_module = TasksTools()
    await tasks_module.initialize()
    print(f"   Tarefas em memória: {len(tasks_module.tasks)}")
    print(f"   Notas em memória: {len(tasks_module.notes)}")
    print()
    
    # 3. Listar tarefas atuais
    if tasks_module.tasks:
        print("📋 Tarefas encontradas:")
        for task in tasks_module.tasks:
            status = "✅" if task['completed'] else "⏳"
            print(f"   {status} #{task['id']} - {task['title']}")
    else:
        print("   ⚠️ Nenhuma tarefa encontrada na memória")
    print()
    
    # 4. Teste de escrita
    print("✍️ Testando escrita de tarefa...")
    result = await tasks_module.create_task(
        title="Teste de Sincronização",
        description="Tarefa criada pelo script de diagnóstico",
        priority="medium"
    )
    print(f"   Resultado: {result}")
    print(f"   Tarefas após criação: {len(tasks_module.tasks)}")
    print()
    
    # 5. Verificar se foi salvo no arquivo
    print("💾 Verificando salvamento no arquivo...")
    await asyncio.sleep(0.5)  # Pequeno delay
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"   Tarefas no arquivo agora: {len(data.get('tasks', []))}")
    
    # Mostrar última tarefa salva
    if data.get('tasks'):
        last_task = data['tasks'][-1]
        print(f"   Última tarefa: #{last_task['id']} - {last_task['title']}")
    print()
    
    # 6. Teste de reload
    print("🔄 Testando reload de outro módulo...")
    tasks_module2 = TasksTools()
    await tasks_module2.initialize()
    print(f"   Tarefas carregadas: {len(tasks_module2.tasks)}")
    print()
    
    print("="*70)
    print("✅ DIAGNÓSTICO CONCLUÍDO")
    print("="*70)
    print()
    
    # Análise
    print("📊 ANÁLISE:")
    if len(tasks_module.tasks) == len(tasks_module2.tasks):
        print("   ✅ Sincronização está funcionando!")
        print("   ✅ Ambas as instâncias têm os mesmos dados")
    else:
        print("   ❌ PROBLEMA: Instâncias desincronizadas")
        print(f"   Instância 1: {len(tasks_module.tasks)} tarefas")
        print(f"   Instância 2: {len(tasks_module2.tasks)} tarefas")
    print()
    
    # Recomendações
    print("💡 RECOMENDAÇÕES:")
    print("   1. Reinicie o API Server (api_server.py)")
    print("   2. A interface web atualizará em 5 segundos")
    print("   3. Se persistir, verifique logs em ./logs/")
    print()


async def corrigir():
    """Força a sincronização entre MCP e API Server"""
    print("="*70)
    print("🔧 CORREÇÃO: Forçando sincronização")
    print("="*70)
    print()
    
    # 1. Carregar do arquivo
    json_path = Path(settings.TASKS_DB_PATH)
    if not json_path.exists():
        print("❌ Arquivo tasks.json não encontrado!")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📂 Arquivo: {json_path}")
    print(f"   Tarefas: {len(data.get('tasks', []))}")
    print(f"   Notas: {len(data.get('notes', []))}")
    print()
    
    # 2. Forçar atualização do timestamp
    from datetime import datetime
    data['last_updated'] = datetime.now().isoformat()
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Arquivo atualizado com timestamp atual")
    print("✅ Reinicie o API Server para aplicar mudanças")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        asyncio.run(corrigir())
    else:
        asyncio.run(diagnostico())
    
    print("Para forçar correção, execute:")
    print("  python diagnostic_tasks.py --fix")
    print()
