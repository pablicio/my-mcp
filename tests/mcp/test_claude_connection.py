#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes de Conexão MCP com Claude
Valida comunicação entre o servidor MCP e o cliente Claude Desktop
"""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.server import MCPPersonalServer
from modules.tasks.tools import TasksTools


class TestClaudeConnection:
    """Testes de conexão e comunicação com Claude Desktop"""
    
    @pytest.fixture
    async def server(self):
        """Fixture para criar servidor MCP"""
        server = MCPPersonalServer()
        await server.initialize()
        return server
    
    @pytest.fixture
    async def tasks_module(self):
        """Fixture para módulo de tarefas"""
        module = TasksTools()
        await module.initialize()
        return module
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Testa se o servidor inicializa corretamente"""
        assert server is not None
        assert server.mcp is not None
        assert len(server.modules) > 0
        assert 'tasks' in server.modules
        
    @pytest.mark.asyncio
    async def test_tools_registration(self, server):
        """Testa se as ferramentas foram registradas"""
        assert len(server.registry.tools) > 0
        
        # Verificar ferramentas principais
        expected_tools = [
            'create_task',
            'list_tasks',
            'complete_task',
            'delete_task',
            'create_note',
            'list_notes',
            'search_tasks'
        ]
        
        for tool_name in expected_tools:
            assert tool_name in server.registry.tools, f"Tool {tool_name} não registrada"
    
    @pytest.mark.asyncio
    async def test_create_task_via_mcp(self, server):
        """Testa criação de tarefa via protocolo MCP"""
        tasks_module = server.modules['tasks']
        
        # Criar tarefa
        result = await tasks_module.create_task(
            title="Teste MCP Connection",
            description="Tarefa criada durante teste de conexão",
            priority="high"
        )
        
        assert "criada com sucesso" in result
        assert len(tasks_module.tasks) > 0
        
        # Verificar tarefa criada
        last_task = tasks_module.tasks[-1]
        assert last_task['title'] == "Teste MCP Connection"
        assert last_task['priority'] == "high"
        assert not last_task['completed']
    
    @pytest.mark.asyncio
    async def test_list_tasks_via_mcp(self, tasks_module):
        """Testa listagem de tarefas via MCP"""
        # Criar algumas tarefas
        await tasks_module.create_task("Tarefa 1", "Descrição 1", "high")
        await tasks_module.create_task("Tarefa 2", "Descrição 2", "medium")
        await tasks_module.create_task("Tarefa 3", "Descrição 3", "low")
        
        # Listar todas
        result = await tasks_module.list_tasks(status="all")
        assert "Tarefa 1" in result
        assert "Tarefa 2" in result
        assert "Tarefa 3" in result
        
        # Listar apenas pendentes
        result_pending = await tasks_module.list_tasks(status="pending")
        assert "⏳" in result_pending
    
    @pytest.mark.asyncio
    async def test_complete_task_via_mcp(self, tasks_module):
        """Testa conclusão de tarefa via MCP"""
        # Criar tarefa
        await tasks_module.create_task("Tarefa para completar", "Teste", "medium")
        task_id = tasks_module.tasks[-1]['id']
        
        # Completar tarefa
        result = await tasks_module.complete_task(task_id)
        assert "concluída" in result.lower()
        
        # Verificar status
        task = next(t for t in tasks_module.tasks if t['id'] == task_id)
        assert task['completed'] is True
        assert task['completed_at'] is not None
    
    @pytest.mark.asyncio
    async def test_search_tasks_via_mcp(self, tasks_module):
        """Testa busca de tarefas via MCP"""
        # Criar tarefas com palavras-chave
        await tasks_module.create_task("Estudar Python", "Curso de Python avançado", "high")
        await tasks_module.create_task("Estudar JavaScript", "Curso de JS", "medium")
        await tasks_module.create_task("Ler livro", "Livro sobre programação", "low")
        
        # Buscar por "Python"
        result = await tasks_module.search_tasks("Python")
        assert "Python" in result
        assert "JavaScript" not in result
        
        # Buscar por "Estudar"
        result = await tasks_module.search_tasks("Estudar")
        assert "Python" in result
        assert "JavaScript" in result
    
    @pytest.mark.asyncio
    async def test_create_note_via_mcp(self, tasks_module):
        """Testa criação de nota via MCP"""
        result = await tasks_module.create_note(
            title="Nota de Teste MCP",
            content="Esta nota foi criada durante teste de conexão MCP",
            tags="teste, mcp, automatizado"
        )
        
        assert "criada com sucesso" in result
        assert len(tasks_module.notes) > 0
        
        # Verificar nota
        note = tasks_module.notes[-1]
        assert note['title'] == "Nota de Teste MCP"
        assert "teste" in note['tags']
    
    @pytest.mark.asyncio
    async def test_data_persistence(self, tasks_module):
        """Testa persistência de dados"""
        # Criar tarefa
        await tasks_module.create_task("Tarefa Persistente", "Teste de persistência", "high")
        task_count_before = len(tasks_module.tasks)
        
        # Salvar dados
        await tasks_module.save_data()
        
        # Criar novo módulo e carregar dados
        new_module = TasksTools()
        await new_module.initialize()
        
        assert len(new_module.tasks) == task_count_before
        assert any(t['title'] == "Tarefa Persistente" for t in new_module.tasks)
    
    @pytest.mark.asyncio
    async def test_error_handling(self, tasks_module):
        """Testa tratamento de erros"""
        # Tentar completar tarefa inexistente
        result = await tasks_module.complete_task(99999)
        assert "não encontrada" in result
        
        # Tentar deletar sem confirmação
        await tasks_module.create_task("Tarefa para deletar", "", "low")
        task_id = tasks_module.tasks[-1]['id']
        result = await tasks_module.delete_task(task_id, confirm=False)
        assert "ATENÇÃO" in result or "confirmação" in result.lower()
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, tasks_module):
        """Testa operações concorrentes"""
        # Criar múltiplas tarefas simultaneamente
        tasks_to_create = [
            ("Tarefa Concorrente 1", "Descrição 1", "high"),
            ("Tarefa Concorrente 2", "Descrição 2", "medium"),
            ("Tarefa Concorrente 3", "Descrição 3", "low"),
        ]
        
        results = await asyncio.gather(*[
            tasks_module.create_task(title, desc, priority)
            for title, desc, priority in tasks_to_create
        ])
        
        # Verificar se todas foram criadas
        assert all("criada com sucesso" in r for r in results)
        assert len([t for t in tasks_module.tasks if "Concorrente" in t['title']]) == 3
    
    def test_server_status(self, server):
        """Testa status do servidor"""
        status = server.get_status()
        
        assert status['status'] == 'running'
        assert 'modules' in status
        assert 'tools_count' in status
        assert status['tools_count'] > 0


class TestClaudeProtocolCompliance:
    """Testes de conformidade com protocolo MCP"""
    
    @pytest.fixture
    async def server(self):
        """Fixture para servidor"""
        server = MCPPersonalServer()
        await server.initialize()
        return server
    
    @pytest.mark.asyncio
    async def test_tool_function_signatures(self, server):
        """Testa se as funções têm assinaturas corretas"""
        tasks_tools = server.modules['tasks'].get_tools()
        
        # Verificar create_task
        import inspect
        sig = inspect.signature(tasks_tools['create_task'])
        params = list(sig.parameters.keys())
        
        assert 'title' in params
        assert 'description' in params
        assert 'priority' in params
        assert 'due_date' in params
    
    @pytest.mark.asyncio
    async def test_tool_return_types(self, server):
        """Testa se as ferramentas retornam strings"""
        tasks_module = server.modules['tasks']
        
        # Todas as ferramentas devem retornar strings
        result = await tasks_module.create_task("Teste", "", "low")
        assert isinstance(result, str)
        
        result = await tasks_module.list_tasks()
        assert isinstance(result, str)
        
        await tasks_module.create_task("Para completar", "", "low")
        task_id = tasks_module.tasks[-1]['id']
        result = await tasks_module.complete_task(task_id)
        assert isinstance(result, str)


class TestClaudeIntegrationScenarios:
    """Testes de cenários de integração com Claude"""
    
    @pytest.fixture
    async def tasks_module(self):
        """Fixture para módulo de tarefas"""
        module = TasksTools()
        await module.initialize()
        # Limpar dados anteriores
        module.tasks = []
        module.notes = []
        await module.save_data()
        return module
    
    @pytest.mark.asyncio
    async def test_user_workflow_create_and_complete(self, tasks_module):
        """Simula workflow completo de usuário via Claude"""
        # Passo 1: Usuário pede para criar tarefa
        result = await tasks_module.create_task(
            title="Estudar MCP Protocol",
            description="Entender como Claude se comunica com servidores MCP",
            priority="high",
            due_date="2025-12-31"
        )
        assert "criada com sucesso" in result
        
        # Passo 2: Usuário lista tarefas
        result = await tasks_module.list_tasks(status="pending")
        assert "Estudar MCP Protocol" in result
        
        # Passo 3: Usuário completa a tarefa
        task_id = tasks_module.tasks[-1]['id']
        result = await tasks_module.complete_task(task_id)
        assert "concluída" in result.lower()
        
        # Passo 4: Usuário verifica tarefas concluídas
        result = await tasks_module.list_tasks(status="completed")
        assert "Estudar MCP Protocol" in result
        assert "✅" in result
    
    @pytest.mark.asyncio
    async def test_user_workflow_with_notes(self, tasks_module):
        """Simula workflow com tarefas e notas"""
        # Criar tarefa
        await tasks_module.create_task("Projeto X", "Desenvolver feature Y", "high")
        
        # Criar nota relacionada
        await tasks_module.create_note(
            title="Ideias para Projeto X",
            content="Implementar autenticação OAuth, adicionar dashboard, melhorar performance",
            tags="projeto-x, ideias, desenvolvimento"
        )
        
        # Buscar tarefa
        result = await tasks_module.search_tasks("Projeto X")
        assert "Projeto X" in result
        
        # Listar notas
        result = await tasks_module.list_notes()
        assert "Ideias para Projeto X" in result


# Funções auxiliares para executar testes
def run_connection_tests():
    """Executa todos os testes de conexão"""
    print("="*60)
    print("🧪 TESTES DE CONEXÃO MCP COM CLAUDE")
    print("="*60)
    
    # Executar pytest
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])


if __name__ == '__main__':
    run_connection_tests()
