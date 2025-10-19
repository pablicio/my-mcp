#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste para a API do MCP Server
Valida todos os endpoints e funcionalidades
"""

import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

API_URL = "http://localhost:5000/api"

class APITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
    
    def print_header(self, text):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}{text}")
        print(f"{Fore.CYAN}{'='*60}")
    
    def print_test(self, name):
        self.total += 1
        print(f"\n{Fore.YELLOW}[TEST {self.total}] {name}")
    
    def print_success(self, message):
        self.passed += 1
        print(f"{Fore.GREEN}✅ PASS: {message}")
    
    def print_error(self, message):
        self.failed += 1
        print(f"{Fore.RED}❌ FAIL: {message}")
    
    def print_info(self, message):
        print(f"{Fore.BLUE}ℹ️  INFO: {message}")
    
    def print_summary(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}RESUMO DOS TESTES")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}Total de testes: {self.total}")
        print(f"{Fore.GREEN}Passou: {self.passed}")
        print(f"{Fore.RED}Falhou: {self.failed}")
        
        if self.failed == 0:
            print(f"\n{Fore.GREEN}🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"\n{Fore.RED}⚠️  ALGUNS TESTES FALHARAM")
        print(f"{Fore.CYAN}{'='*60}\n")
    
    def test_status(self):
        """Testa endpoint de status"""
        self.print_test("Status do Servidor")
        
        try:
            response = requests.get(f"{API_URL}/status", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'running':
                    self.print_success("Servidor está rodando")
                else:
                    self.print_error("Status inesperado")
                
                if data.get('initialized'):
                    self.print_success("Módulos inicializados")
                else:
                    self.print_error("Módulos não inicializados")
                
                stats = data.get('stats', {})
                self.print_info(f"Tarefas: {stats.get('tasks', 0)}")
                self.print_info(f"Notas: {stats.get('notes', 0)}")
                
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_list_tasks(self):
        """Testa listagem de tarefas"""
        self.print_test("Listar Tarefas")
        
        try:
            response = requests.get(f"{API_URL}/tasks", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                tasks = data.get('tasks', [])
                
                self.print_success(f"Listagem bem-sucedida: {len(tasks)} tarefas")
                
                if 'total' in data:
                    self.print_info(f"Total: {data['total']}")
                if 'pending' in data:
                    self.print_info(f"Pendentes: {data['pending']}")
                if 'completed' in data:
                    self.print_info(f"Concluídas: {data['completed']}")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_create_task(self):
        """Testa criação de tarefa"""
        self.print_test("Criar Tarefa")
        
        task_data = {
            'title': f'Tarefa de Teste {datetime.now().strftime("%H:%M:%S")}',
            'description': 'Tarefa criada pelo script de teste',
            'priority': 'medium',
            'due_date': '2025-12-31'
        }
        
        try:
            response = requests.post(
                f"{API_URL}/tasks",
                json=task_data,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.print_success("Tarefa criada com sucesso")
                    
                    if 'task' in data:
                        task = data['task']
                        self.print_info(f"ID: {task.get('id')}")
                        self.print_info(f"Título: {task.get('title')}")
                        return task.get('id')
                else:
                    self.print_error("Success = False na resposta")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
        
        return None
    
    def test_complete_task(self, task_id):
        """Testa conclusão de tarefa"""
        if not task_id:
            self.print_test("Completar Tarefa - SKIPPED (sem ID)")
            return
        
        self.print_test(f"Completar Tarefa #{task_id}")
        
        try:
            response = requests.post(
                f"{API_URL}/tasks/{task_id}/complete",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.print_success(f"Tarefa #{task_id} concluída")
                else:
                    self.print_error("Success = False")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_delete_task(self, task_id):
        """Testa exclusão de tarefa"""
        if not task_id:
            self.print_test("Deletar Tarefa - SKIPPED (sem ID)")
            return
        
        self.print_test(f"Deletar Tarefa #{task_id}")
        
        try:
            response = requests.delete(
                f"{API_URL}/tasks/{task_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.print_success(f"Tarefa #{task_id} deletada")
                else:
                    self.print_error("Success = False")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_list_notes(self):
        """Testa listagem de notas"""
        self.print_test("Listar Notas")
        
        try:
            response = requests.get(f"{API_URL}/notes", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                notes = data.get('notes', [])
                
                self.print_success(f"Listagem bem-sucedida: {len(notes)} notas")
                
                if 'total' in data:
                    self.print_info(f"Total: {data['total']}")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_create_note(self):
        """Testa criação de nota"""
        self.print_test("Criar Nota")
        
        note_data = {
            'title': f'Nota de Teste {datetime.now().strftime("%H:%M:%S")}',
            'content': 'Esta é uma nota criada pelo script de teste automático.',
            'tags': 'teste, automatico'
        }
        
        try:
            response = requests.post(
                f"{API_URL}/notes",
                json=note_data,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    self.print_success("Nota criada com sucesso")
                    
                    if 'note' in data:
                        note = data['note']
                        self.print_info(f"ID: {note.get('id')}")
                        self.print_info(f"Título: {note.get('title')}")
                else:
                    self.print_error("Success = False")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_search_tasks(self):
        """Testa busca de tarefas"""
        self.print_test("Buscar Tarefas")
        
        try:
            response = requests.get(
                f"{API_URL}/search/tasks",
                params={'q': 'teste'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                tasks = data.get('tasks', [])
                
                self.print_success(f"Busca realizada: {len(tasks)} resultados")
                self.print_info(f"Query: {data.get('query')}")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_logs(self):
        """Testa endpoint de logs"""
        self.print_test("Logs do Servidor")
        
        try:
            response = requests.get(
                f"{API_URL}/logs",
                params={'limit': 10},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                logs = data.get('logs', [])
                
                self.print_success(f"Logs recuperados: {len(logs)} linhas")
                
                if 'total' in data:
                    self.print_info(f"Total de logs: {data['total']}")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_metrics(self):
        """Testa endpoint de métricas"""
        self.print_test("Métricas do Sistema")
        
        try:
            response = requests.get(f"{API_URL}/metrics", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                self.print_success("Métricas recuperadas")
                
                if 'tasks' in data:
                    tasks = data['tasks']
                    self.print_info(f"Total de tarefas: {tasks.get('total')}")
                    self.print_info(f"Taxa de conclusão: {tasks.get('completion_rate')}%")
                
                if 'priority' in data:
                    priority = data['priority']
                    self.print_info(f"Alta prioridade: {priority.get('high')}")
            else:
                self.print_error(f"Status code: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Exceção: {e}")
    
    def test_filters(self):
        """Testa filtros de tarefas"""
        self.print_test("Filtros de Tarefas")
        
        filters = ['all', 'pending', 'completed']
        
        for filter_type in filters:
            try:
                response = requests.get(
                    f"{API_URL}/tasks",
                    params={'status': filter_type},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('tasks', []))
                    self.print_success(f"Filtro '{filter_type}': {count} tarefas")
                else:
                    self.print_error(f"Filtro '{filter_type}' falhou")
                    
            except Exception as e:
                self.print_error(f"Filtro '{filter_type}': {e}")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        self.print_header("🧪 INICIANDO TESTES DA API DO MCP SERVER")
        
        print(f"\n{Fore.WHITE}API URL: {API_URL}")
        print(f"{Fore.WHITE}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Testes básicos
        self.test_status()
        time.sleep(0.5)
        
        # Testes de tarefas
        self.test_list_tasks()
        time.sleep(0.5)
        
        task_id = self.test_create_task()
        time.sleep(0.5)
        
        self.test_complete_task(task_id)
        time.sleep(0.5)
        
        self.test_delete_task(task_id)
        time.sleep(0.5)
        
        # Testes de notas
        self.test_list_notes()
        time.sleep(0.5)
        
        self.test_create_note()
        time.sleep(0.5)
        
        # Testes de busca e filtros
        self.test_search_tasks()
        time.sleep(0.5)
        
        self.test_filters()
        time.sleep(0.5)
        
        # Testes de logs e métricas
        self.test_logs()
        time.sleep(0.5)
        
        self.test_metrics()
        
        # Resumo
        self.print_summary()

def main():
    """Função principal"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}MCP SERVER - SCRIPT DE TESTE AUTOMATIZADO")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    # Verificar se servidor está rodando
    print(f"{Fore.YELLOW}Verificando conexão com o servidor...")
    
    try:
        response = requests.get(f"{API_URL}/status", timeout=3)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ Servidor está rodando!\n")
        else:
            print(f"{Fore.RED}❌ Servidor retornou status {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}❌ Não foi possível conectar ao servidor!")
        print(f"{Fore.RED}   Certifique-se que o servidor está rodando em {API_URL}")
        print(f"{Fore.RED}   Erro: {e}\n")
        return
    
    # Executar testes
    tester = APITester()
    tester.run_all_tests()

if __name__ == '__main__':
    main()
