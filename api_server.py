#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST para Interface Web do MCP Server
Fornece endpoints para a interface HTML se conectar aos dados reais
"""

import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Importar módulos do MCP
import sys
sys.path.insert(0, str(Path(__file__).parent))

from modules.tasks.tools import TasksTools
from config.settings import settings

# Configurar logging aprimorado
log_dir = Path('./logs')
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'api_server.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)  # Permitir CORS para desenvolvimento

# Instâncias dos módulos
tasks_module = None

@app.route('/')
def index():
    """Serve a página principal"""
    logger.info("📄 Servindo página principal")
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Serve o CSS"""
    return send_from_directory('.', 'styles.css')

@app.route('/app.js')
def app_js():
    """Serve o JavaScript"""
    return send_from_directory('.', 'app.js')

@app.route('/api/status')
def get_status():
    """Retorna status do servidor com métricas detalhadas"""
    try:
        log_file = Path('./logs/mcp_server.log')
        api_log_file = Path('./logs/api_server.log')
        log_exists = log_file.exists() or api_log_file.exists()
        
        # Ler últimas linhas do log
        last_logs = []
        if api_log_file.exists():
            with open(api_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_logs = lines[-10:] if len(lines) > 10 else lines
        elif log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_logs = lines[-10:] if len(lines) > 10 else lines
        
        # Estatísticas das tarefas
        task_count = 0
        note_count = 0
        completed_count = 0
        
        if tasks_module:
            task_count = len([t for t in tasks_module.tasks if not t['completed']])
            completed_count = len([t for t in tasks_module.tasks if t['completed']])
            note_count = len(tasks_module.notes)
        
        status_data = {
            'status': 'running',
            'initialized': tasks_module is not None,
            'modules': {
                'tasks': tasks_module is not None,
                'filesystem': True,
                'calendar': True  # Sempre disponível
            },
            'stats': {
                'tasks': task_count,
                'completed': completed_count,
                'notes': note_count,
                'tools': 14,
                'total_tasks': task_count + completed_count
            },
            'logs': {
                'exists': log_exists,
                'last_lines': [line.strip() for line in last_logs]
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.debug(f"📊 Status: {task_count} tarefas ativas, {completed_count} concluídas, {note_count} notas")
        return jsonify(status_data)
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar status: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks')
def get_tasks():
    """Lista todas as tarefas com filtros"""
    try:
        if not tasks_module:
            logger.warning("⚠️ Módulo de tarefas não inicializado")
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        status = request.args.get('status', 'all')
        limit = int(request.args.get('limit', 50))
        
        filtered_tasks = tasks_module.tasks
        
        if status == 'pending':
            filtered_tasks = [t for t in tasks_module.tasks if not t['completed']]
        elif status == 'completed':
            filtered_tasks = [t for t in tasks_module.tasks if t['completed']]
        
        # Ordenar por prioridade e data
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        filtered_tasks = sorted(
            filtered_tasks,
            key=lambda x: (x['completed'], priority_order.get(x['priority'], 1))
        )
        
        logger.info(f"📋 Listando {len(filtered_tasks)} tarefas (filtro: {status})")
        
        return jsonify({
            'tasks': filtered_tasks[:limit],
            'total': len(tasks_module.tasks),
            'filtered': len(filtered_tasks),
            'pending': len([t for t in tasks_module.tasks if not t['completed']]),
            'completed': len([t for t in tasks_module.tasks if t['completed']])
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar tarefas: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Cria uma nova tarefa"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        data = request.get_json()
        title = data.get('title', '')
        
        logger.info(f"➕ Criando tarefa: '{title}' (prioridade: {data.get('priority', 'medium')})")
        
        result = asyncio.run(tasks_module.create_task(
            title=title,
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date', '')
        ))
        
        logger.info(f"✅ Tarefa criada: #{tasks_module.tasks[-1]['id']} - {title}")
        
        return jsonify({
            'success': True,
            'message': result,
            'task': tasks_module.tasks[-1] if tasks_module.tasks else None
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar tarefa: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Marca tarefa como concluída"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        # Encontrar título da tarefa para log
        task = next((t for t in tasks_module.tasks if t['id'] == task_id), None)
        task_title = task['title'] if task else f"#{task_id}"
        
        logger.info(f"✓ Completando tarefa: {task_title}")
        result = asyncio.run(tasks_module.complete_task(task_id))
        
        logger.info(f"✅ Tarefa concluída: {task_title}")
        
        return jsonify({
            'success': True,
            'message': result
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao completar tarefa #{task_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deleta uma tarefa"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        # Encontrar título da tarefa para log
        task = next((t for t in tasks_module.tasks if t['id'] == task_id), None)
        task_title = task['title'] if task else f"#{task_id}"
        
        logger.info(f"🗑️ Deletando tarefa: {task_title}")
        result = asyncio.run(tasks_module.delete_task(task_id, confirm=True))
        
        logger.info(f"✅ Tarefa deletada: {task_title}")
        
        return jsonify({
            'success': True,
            'message': result
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao deletar tarefa #{task_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes')
def get_notes():
    """Lista todas as notas"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        limit = int(request.args.get('limit', 20))
        
        # Ordenar por data
        sorted_notes = sorted(
            tasks_module.notes,
            key=lambda x: x['created_at'],
            reverse=True
        )
        
        logger.info(f"📝 Listando {len(sorted_notes)} notas")
        
        return jsonify({
            'notes': sorted_notes[:limit],
            'total': len(tasks_module.notes)
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar notas: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Cria uma nova nota"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        data = request.get_json()
        title = data.get('title', '')
        
        logger.info(f"➕ Criando nota: '{title}'")
        
        result = asyncio.run(tasks_module.create_note(
            title=title,
            content=data.get('content', ''),
            tags=data.get('tags', '')
        ))
        
        logger.info(f"✅ Nota criada: {title}")
        
        return jsonify({
            'success': True,
            'message': result,
            'note': tasks_module.notes[-1] if tasks_module.notes else None
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar nota: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Retorna logs do servidor com filtros avançados"""
    try:
        log_file = Path('./logs/api_server.log')
        
        if not log_file.exists():
            logger.warning("⚠️ Arquivo de log não encontrado")
            return jsonify({'logs': [], 'total': 0})
        
        limit = int(request.args.get('limit', 100))
        level = request.args.get('level', 'all').upper()
        
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filtrar por nível se especificado
        if level != 'ALL':
            lines = [line for line in lines if f'[{level}]' in line]
        
        recent_logs = lines[-limit:] if len(lines) > limit else lines
        
        logger.debug(f"📊 Retornando {len(recent_logs)} logs (filtro: {level})")
        
        return jsonify({
            'logs': [line.strip() for line in recent_logs],
            'total': len(lines),
            'filtered': len(recent_logs)
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar logs: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/tasks')
def search_tasks():
    """Busca tarefas por texto"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        query = request.args.get('q', '').lower()
        
        if not query:
            return jsonify({'tasks': [], 'count': 0})
        
        logger.info(f"🔍 Buscando tarefas: '{query}'")
        
        matches = []
        for task in tasks_module.tasks:
            if (query in task['title'].lower() or 
                query in task['description'].lower()):
                matches.append(task)
        
        logger.info(f"✅ Encontradas {len(matches)} tarefas para '{query}'")
        
        return jsonify({
            'tasks': matches,
            'query': query,
            'count': len(matches)
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar tarefas: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    """Retorna métricas detalhadas do sistema"""
    try:
        if not tasks_module:
            return jsonify({'error': 'Tasks module not initialized'}), 500
        
        # Calcular métricas
        total_tasks = len(tasks_module.tasks)
        pending_tasks = len([t for t in tasks_module.tasks if not t['completed']])
        completed_tasks = len([t for t in tasks_module.tasks if t['completed']])
        
        high_priority = len([t for t in tasks_module.tasks if t['priority'] == 'high' and not t['completed']])
        medium_priority = len([t for t in tasks_module.tasks if t['priority'] == 'medium' and not t['completed']])
        low_priority = len([t for t in tasks_module.tasks if t['priority'] == 'low' and not t['completed']])
        
        # Taxa de conclusão
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        metrics = {
            'tasks': {
                'total': total_tasks,
                'pending': pending_tasks,
                'completed': completed_tasks,
                'completion_rate': round(completion_rate, 2)
            },
            'priority': {
                'high': high_priority,
                'medium': medium_priority,
                'low': low_priority
            },
            'notes': {
                'total': len(tasks_module.notes)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("📊 Métricas consultadas")
        return jsonify(metrics)
        
    except Exception as e:
        logger.error(f"❌ Erro ao calcular métricas: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

def initialize_modules():
    """Inicializa os módulos do MCP com logging detalhado"""
    global tasks_module
    
    try:
        logger.info("="*60)
        logger.info("🚀 Inicializando módulos do MCP Server")
        logger.info("="*60)
        
        tasks_module = TasksTools()
        asyncio.run(tasks_module.initialize())
        
        task_count = len(tasks_module.tasks)
        note_count = len(tasks_module.notes)
        
        logger.info(f"✅ Módulo de tarefas inicializado")
        logger.info(f"📊 Estatísticas iniciais:")
        logger.info(f"   - Tarefas: {task_count}")
        logger.info(f"   - Notas: {note_count}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar módulos: {e}", exc_info=True)
        raise

def main():
    """Inicia o servidor API com configurações aprimoradas"""
    print("="*60)
    print("🚀 MCP SERVER - API REST")
    print("="*60)
    print()
    
    # Inicializar módulos
    initialize_modules()
    
    print()
    print("📡 Servidor iniciando...")
    print("🌐 Interface: http://localhost:5000")
    print("📊 API: http://localhost:5000/api/")
    print()
    print("Endpoints disponíveis:")
    print("  GET  /api/status          - Status do servidor")
    print("  GET  /api/tasks           - Listar tarefas")
    print("  POST /api/tasks           - Criar tarefa")
    print("  POST /api/tasks/:id/complete - Completar tarefa")
    print("  DELETE /api/tasks/:id     - Deletar tarefa")
    print("  GET  /api/notes           - Listar notas")
    print("  POST /api/notes           - Criar nota")
    print("  GET  /api/logs            - Logs do servidor")
    print("  GET  /api/search/tasks    - Buscar tarefas")
    print("  GET  /api/metrics         - Métricas do sistema")
    print()
    print("📝 Logs salvos em: ./logs/api_server.log")
    print("Pressione Ctrl+C para parar")
    print("="*60)
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )

if __name__ == '__main__':
    main()
