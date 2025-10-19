#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido da API REST
Verifica se todos os endpoints estão funcionando corretamente
"""

import requests
import json
import time
from datetime import datetime

API_URL = 'http://localhost:5000/api'

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_status():
    """Testa endpoint de status"""
    print_header("Testando GET /api/status")
    
    try:
        response = requests.get(f'{API_URL}/status', timeout=5)
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Servidor: {data['status']}")
        print_info(f"Inicializado: {data['initialized']}")
        print_info(f"Tarefas: {data['stats']['tasks']}")
        print_info(f"Notas: {data['stats']['notes']}")
        print_info(f"Ferramentas: {data['stats']['tools']}")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_list_tasks():
    """Testa listagem de tarefas"""
    print_header("Testando GET /api/tasks")
    
    try:
        response = requests.get(f'{API_URL}/tasks', timeout=5)
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Total de tarefas: {data['total']}")
        print_info(f"Tarefas filtradas: {data['filtered']}")
        
        if data['tasks']:
            print_info("\nPrimeiras tarefas:")
            for task in data['tasks'][:3]:
                status = "✅" if task['completed'] else "⏳"
                print(f"  {status} #{task['id']} {task['title']} [{task['priority']}]")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_create_task():
    """Testa criação de tarefa"""
    print_header("Testando POST /api/tasks")
    
    task_data = {
        "title": f"Tarefa de Teste - {datetime.now().strftime('%H:%M:%S')}",
        "description": "Criada automaticamente pelo script de testes",
        "priority": "medium",
        "due_date": ""
    }
    
    try:
        response = requests.post(
            f'{API_URL}/tasks',
            json=task_data,
            timeout=5
        )
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Mensagem: {data['message']}")
        print_info(f"Total de tarefas agora: {len(data['tasks'])}")
        
        # Retornar ID da última tarefa criada
        if data['tasks']:
            last_task = data['tasks'][-1]
            print_info(f"ID da tarefa criada: {last_task['id']}")
            return last_task['id']
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_complete_task(task_id):
    """Testa conclusão de tarefa"""
    print_header(f"Testando POST /api/tasks/{task_id}/complete")
    
    try:
        response = requests.post(
            f'{API_URL}/tasks/{task_id}/complete',
            timeout=5
        )
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Mensagem: {data['message']}")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_delete_task(task_id):
    """Testa deleção de tarefa"""
    print_header(f"Testando DELETE /api/tasks/{task_id}")
    
    try:
        response = requests.delete(
            f'{API_URL}/tasks/{task_id}',
            timeout=5
        )
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Mensagem: {data['message']}")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_list_notes():
    """Testa listagem de notas"""
    print_header("Testando GET /api/notes")
    
    try:
        response = requests.get(f'{API_URL}/notes', timeout=5)
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Total de notas: {data['total']}")
        
        if data['notes']:
            print_info("\nPrimeiras notas:")
            for note in data['notes'][:3]:
                print(f"  📝 #{note['id']} {note['title']}")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_logs():
    """Testa endpoint de logs"""
    print_header("Testando GET /api/logs")
    
    try:
        response = requests.get(f'{API_URL}/logs?limit=10', timeout=5)
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Total de logs: {data['total']}")
        print_info(f"Últimas linhas retornadas: {len(data['logs'])}")
        
        if data['logs']:
            print_info("\nÚltimas 3 linhas:")
            for log in data['logs'][-3:]:
                print(f"  {log}")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_search_tasks():
    """Testa busca de tarefas"""
    print_header("Testando GET /api/search/tasks")
    
    try:
        response = requests.get(f'{API_URL}/search/tasks?q=teste', timeout=5)
        data = response.json()
        
        print_success(f"Status: {response.status_code}")
        print_info(f"Query: {data['query']}")
        print_info(f"Resultados: {data['count']}")
        
        if data['tasks']:
            print_info("\nTarefas encontradas:")
            for task in data['tasks']:
                print(f"  #{task['id']} {task['title']}")
        
        return True
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  🧪 TESTE DA API REST DO MCP SERVER")
    print("="*60)
    print("\n⚠️  Certifique-se de que o servidor está rodando!")
    print("   Execute: python api_server.py")
    print("\n⏳ Aguardando 2 segundos...")
    time.sleep(2)
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Teste 1: Status
    if test_status():
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("Servidor não está rodando! Execute: python api_server.py")
        return
    
    time.sleep(1)
    
    # Teste 2: Listar tarefas
    if test_list_tasks():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    time.sleep(1)
    
    # Teste 3: Criar tarefa
    task_id = test_create_task()
    if task_id:
        results['passed'] += 1
    else:
        results['failed'] += 1
        task_id = None
    
    time.sleep(1)
    
    # Teste 4: Completar tarefa (se criou uma)
    if task_id:
        if test_complete_task(task_id):
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        time.sleep(1)
    
    # Teste 5: Deletar tarefa (se criou uma)
    if task_id:
        if test_delete_task(task_id):
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        time.sleep(1)
    
    # Teste 6: Listar notas
    if test_list_notes():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    time.sleep(1)
    
    # Teste 7: Logs
    if test_logs():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    time.sleep(1)
    
    # Teste 8: Busca
    if test_search_tasks():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    print(f"\n✅ Passou: {results['passed']}")
    print(f"❌ Falhou: {results['failed']}")
    print(f"📊 Total: {results['passed'] + results['failed']}")
    
    if results['failed'] == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ A API está funcionando perfeitamente!")
        print("\n🌐 Acesse a interface web em: http://localhost:5000")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("\n💡 Verifique se o servidor está rodando corretamente")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
