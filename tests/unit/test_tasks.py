"""
🧪 Testes para módulo de tarefas.
"""

import pytest
import asyncio
import json
from pathlib import Path
from modules.tasks.tools import TasksTools

@pytest.fixture
def tasks_tool(tmp_path):
    """Fixture para criar instância de TasksTools com BD temporário."""
    from config.settings import settings
    
    # Usar caminho temporário
    original_path = settings.TASKS_DB_PATH
    settings.TASKS_DB_PATH = str(tmp_path / "test_tasks.json")
    
    tool = TasksTools()
    
    yield tool
    
    # Restaurar caminho original
    settings.TASKS_DB_PATH = original_path

@pytest.mark.asyncio
async def test_is_available(tasks_tool):
    """Testa se o módulo está disponível."""
    is_available = await tasks_tool.is_available()
    assert is_available is True

@pytest.mark.asyncio
async def test_initialize(tasks_tool):
    """Testa inicialização do módulo."""
    await tasks_tool.initialize()
    assert tasks_tool.initialized is True
    assert isinstance(tasks_tool.tasks, list)
    assert isinstance(tasks_tool.notes, list)

@pytest.mark.asyncio
async def test_create_task(tasks_tool):
    """Testa criação de tarefa."""
    await tasks_tool.initialize()
    
    result = await tasks_tool.create_task(
        title="Test Task",
        description="Test description",
        priority="high"
    )
    
    assert "sucesso" in result.lower()
    assert len(tasks_tool.tasks) == 1
    assert tasks_tool.tasks[0]["title"] == "Test Task"
    assert tasks_tool.tasks[0]["priority"] == "high"
    assert tasks_tool.tasks[0]["completed"] is False

@pytest.mark.asyncio
async def test_list_tasks(tasks_tool):
    """Testa listagem de tarefas."""
    await tasks_tool.initialize()
    
    # Criar algumas tarefas
    await tasks_tool.create_task("Task 1", priority="high")
    await tasks_tool.create_task("Task 2", priority="low")
    
    result = await tasks_tool.list_tasks()
    
    assert "Task 1" in result
    assert "Task 2" in result
    assert "🔴" in result  # Ícone de prioridade alta
    assert "🟢" in result  # Ícone de prioridade baixa

@pytest.mark.asyncio
async def test_complete_task(tasks_tool):
    """Testa conclusão de tarefa."""
    await tasks_tool.initialize()
    
    # Criar tarefa
    await tasks_tool.create_task("Task to complete")
    
    # Completar
    result = await tasks_tool.complete_task(1)
    
    assert "concluída" in result.lower() or "🎉" in result
    assert tasks_tool.tasks[0]["completed"] is True
    assert tasks_tool.tasks[0]["completed_at"] is not None

@pytest.mark.asyncio
async def test_delete_task(tasks_tool):
    """Testa deleção de tarefa."""
    await tasks_tool.initialize()
    
    # Criar tarefa
    await tasks_tool.create_task("Task to delete")
    assert len(tasks_tool.tasks) == 1
    
    # Tentar deletar sem confirmação
    result = await tasks_tool.delete_task(1, confirm=False)
    assert "confirm=True" in result
    assert len(tasks_tool.tasks) == 1
    
    # Deletar com confirmação
    result = await tasks_tool.delete_task(1, confirm=True)
    assert "deletada" in result.lower()
    assert len(tasks_tool.tasks) == 0

@pytest.mark.asyncio
async def test_create_note(tasks_tool):
    """Testa criação de nota."""
    await tasks_tool.initialize()
    
    result = await tasks_tool.create_note(
        title="Test Note",
        content="This is a test note",
        tags="test,example"
    )
    
    assert "sucesso" in result.lower()
    assert len(tasks_tool.notes) == 1
    assert tasks_tool.notes[0]["title"] == "Test Note"
    assert "test" in tasks_tool.notes[0]["tags"]

@pytest.mark.asyncio
async def test_search_tasks(tasks_tool):
    """Testa busca de tarefas."""
    await tasks_tool.initialize()
    
    # Criar tarefas
    await tasks_tool.create_task("Python coding", "Write Python code")
    await tasks_tool.create_task("JavaScript coding", "Write JS code")
    await tasks_tool.create_task("Meeting", "Team meeting")
    
    # Buscar
    result = await tasks_tool.search_tasks("coding")
    
    assert "Python" in result or "python" in result.lower()
    assert "JavaScript" in result or "javascript" in result.lower()
    assert "Meeting" not in result

def test_get_tools(tasks_tool):
    """Testa se as ferramentas são retornadas."""
    tools = tasks_tool.get_tools()
    
    assert "create_task" in tools
    assert "list_tasks" in tools
    assert "complete_task" in tools
    assert "delete_task" in tools
    assert "create_note" in tools
    assert "list_notes" in tools
    assert "search_tasks" in tools
