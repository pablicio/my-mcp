#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor em tempo real do MCP Server.
Mostra status, logs e atividade do servidor.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings

def clear_screen():
    """Limpa a tela."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime cabeçalho."""
    print("="*80)
    print(" 📊 MONITOR MCP SERVER - ATUALIZAÇÃO EM TEMPO REAL".center(80))
    print("="*80)
    print(f" Atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
    print("="*80)

def check_server_running():
    """Verifica se o servidor está rodando."""
    # No Windows, verificar processos Python
    if os.name == 'nt':
        import subprocess
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True
            )
            return 'python.exe' in result.stdout.lower()
        except:
            return False
    return True

def get_log_stats():
    """Obtém estatísticas do log."""
    log_file = Path(settings.LOG_FILE)
    
    if not log_file.exists():
        return {
            'exists': False,
            'size': 0,
            'lines': 0,
            'last_modified': None
        }
    
    stats = log_file.stat()
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            total_lines = len(lines)
    except:
        total_lines = 0
        lines = []
    
    return {
        'exists': True,
        'size': stats.st_size,
        'lines': total_lines,
        'last_modified': datetime.fromtimestamp(stats.st_mtime),
        'recent_lines': lines[-10:] if lines else []
    }

def get_tasks_stats():
    """Obtém estatísticas das tarefas."""
    tasks_file = Path(settings.TASKS_DB_PATH)
    
    if not tasks_file.exists():
        return {
            'exists': False,
            'total': 0,
            'pending': 0,
            'completed': 0
        }
    
    try:
        with open(tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])
            
            return {
                'exists': True,
                'total': len(tasks),
                'pending': sum(1 for t in tasks if not t.get('completed', False)),
                'completed': sum(1 for t in tasks if t.get('completed', False))
            }
    except:
        return {
            'exists': True,
            'total': 0,
            'pending': 0,
            'completed': 0
        }

def format_size(size_bytes):
    """Formata tamanho de arquivo."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def print_status():
    """Imprime status completo."""
    clear_screen()
    print_header()
    
    # Status do servidor
    print("\n┌─ 🚀 STATUS DO SERVIDOR")
    print("│")
    
    server_running = check_server_running()
    status_icon = "✅" if server_running else "❌"
    status_text = "RODANDO" if server_running else "PARADO"
    print(f"│  {status_icon} Servidor: {status_text}")
    
    # Configurações
    print("│")
    print(f"│  🔧 Debug Mode: {'✅ Ativo' if settings.DEBUG else '❌ Inativo'}")
    print(f"│  📂 Diretórios: {len(settings.get_allowed_directories())} permitidos")
    
    # Logs
    print("\n├─ 📝 LOGS")
    print("│")
    
    log_stats = get_log_stats()
    if log_stats['exists']:
        print(f"│  ✅ Arquivo: {settings.LOG_FILE}")
        print(f"│  📊 Tamanho: {format_size(log_stats['size'])}")
        print(f"│  📄 Linhas: {log_stats['lines']}")
        print(f"│  🕐 Modificado: {log_stats['last_modified'].strftime('%H:%M:%S')}")
    else:
        print(f"│  ❌ Arquivo de log não existe")
        print(f"│  ℹ️  Será criado quando o servidor iniciar")
    
    # Tarefas
    print("\n├─ 📋 TAREFAS")
    print("│")
    
    tasks_stats = get_tasks_stats()
    if tasks_stats['exists']:
        print(f"│  ✅ Banco: {settings.TASKS_DB_PATH}")
        print(f"│  📊 Total: {tasks_stats['total']}")
        print(f"│  ⏳ Pendentes: {tasks_stats['pending']}")
        print(f"│  ✅ Concluídas: {tasks_stats['completed']}")
    else:
        print(f"│  ❌ Banco de dados não existe")
        print(f"│  ℹ️  Será criado na primeira tarefa")
    
    # Últimos logs
    if log_stats['exists'] and log_stats['recent_lines']:
        print("\n└─ 📜 ÚLTIMAS LINHAS DO LOG")
        print()
        for line in log_stats['recent_lines']:
            line = line.strip()
            if line:
                # Colorir por tipo
                if 'ERROR' in line:
                    print(f"   ❌ {line[:75]}")
                elif 'WARNING' in line:
                    print(f"   ⚠️  {line[:75]}")
                elif 'INFO' in line:
                    print(f"   ℹ️  {line[:75]}")
                else:
                    print(f"      {line[:75]}")
    
    print("\n" + "="*80)
    print(" Pressione Ctrl+C para sair | Atualiza a cada 2 segundos".center(80))
    print("="*80)

def monitor():
    """Monitora continuamente o servidor."""
    try:
        while True:
            print_status()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor encerrado")
        sys.exit(0)

if __name__ == "__main__":
    print("\n🚀 Iniciando monitor...")
    print("⏳ Carregando dados...\n")
    time.sleep(1)
    
    try:
        monitor()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
