"""
✅ Sistema simples de tarefas e notas.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from modules.base import BaseModule
from config.settings import settings
from utils.validators import validate_string

class TasksTools(BaseModule):
    """Módulo de gerenciamento de tarefas e notas."""

    def __init__(self):
        super().__init__()
        self.db_path = Path(settings.TASKS_DB_PATH)
        self.tasks = []
        self.notes = []
        self.next_task_id = 1
        self.next_note_id = 1

    async def is_available(self) -> bool:
        """Sempre disponível - usa armazenamento local."""
        return True

    async def initialize(self):
        """Inicializa o sistema de tarefas."""
        try:
            # Criar diretório se não existir
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # Carregar dados existentes
            await self.load_data()

            self.initialized = True
            self.logger.info(f"Tasks inicializado com {len(self.tasks)} tarefas e {len(self.notes)} notas")

        except Exception as e:
            self.logger.error(f"Erro ao inicializar Tasks: {e}")
            raise

    def get_tools(self) -> Dict[str, callable]:
        """Retorna as ferramentas de tarefas."""
        return {
            "create_task": self.create_task,
            "list_tasks": self.list_tasks,
            "complete_task": self.complete_task,
            "delete_task": self.delete_task,
            "create_note": self.create_note,
            "list_notes": self.list_notes,
            "search_tasks": self.search_tasks
        }

    async def load_data(self):
        """Carrega dados do arquivo JSON."""
        try:
            if self.db_path.exists():
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.notes = data.get('notes', [])
                    self.next_task_id = data.get('next_task_id', 1)
                    self.next_note_id = data.get('next_note_id', 1)
                    
                    # Atualizar IDs se necessário
                    if self.tasks:
                        max_task_id = max(t['id'] for t in self.tasks)
                        self.next_task_id = max(self.next_task_id, max_task_id + 1)
                    if self.notes:
                        max_note_id = max(n['id'] for n in self.notes)
                        self.next_note_id = max(self.next_note_id, max_note_id + 1)
            else:
                self.tasks = []
                self.notes = []
                await self.save_data()
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            self.tasks = []
            self.notes = []

    async def save_data(self):
        """Salva dados no arquivo JSON."""
        try:
            data = {
                'tasks': self.tasks,
                'notes': self.notes,
                'next_task_id': self.next_task_id,
                'next_note_id': self.next_note_id,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados: {e}")

    async def create_task(self, title: str, description: str = "", priority: str = "medium", due_date: str = "") -> str:
        """
        Cria uma nova tarefa.

        Args:
            title: Título da tarefa
            description: Descrição detalhada
            priority: Prioridade (low, medium, high)
            due_date: Data limite opcional, formato ISO

        Returns:
            Confirmação da criação
        """
        try:
            title = validate_string(title, max_length=200)
            description = validate_string(description, max_length=1000)

            if priority not in ['low', 'medium', 'high']:
                priority = 'medium'

            task_id = self.next_task_id
            self.next_task_id += 1

            task = {
                'id': task_id,
                'title': title,
                'description': description,
                'priority': priority,
                'due_date': due_date,
                'completed': False,
                'created_at': datetime.now().isoformat(),
                'completed_at': None
            }

            self.tasks.append(task)
            await self.save_data()

            self.logger.info(f"Tarefa criada: {title}")
            return f"Tarefa #{task_id} '{title}' criada com sucesso"

        except Exception as e:
            self.logger.error(f"Erro ao criar tarefa: {e}")
            return f"Erro ao criar tarefa: {str(e)}"

    async def list_tasks(self, status: str = "all", limit: int = 20) -> str:
        """
        Lista tarefas.

        Args:
            status: Filtro de status (all, pending, completed)
            limit: Número máximo de tarefas

        Returns:
            Lista formatada de tarefas
        """
        try:
            filtered_tasks = self.tasks

            if status == "pending":
                filtered_tasks = [t for t in self.tasks if not t['completed']]
            elif status == "completed":
                filtered_tasks = [t for t in self.tasks if t['completed']]

            # Ordenar por prioridade e data
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            filtered_tasks = sorted(filtered_tasks, 
                                  key=lambda x: (x['completed'], priority_order.get(x['priority'], 1)))

            if not filtered_tasks:
                return f"Nenhuma tarefa encontrada com status '{status}'"

            result = f"Tarefas ({status}):\n"
            for task in filtered_tasks[:limit]:
                status_icon = "✅" if task['completed'] else "⏳"
                priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(task['priority'], '⚪')

                result += f"{status_icon} #{task['id']} {priority_icon} {task['title']}\n"

                if task['description']:
                    result += f"   {task['description'][:100]}{'...' if len(task['description']) > 100 else ''}\n"

                if task['due_date']:
                    result += f"   📅 Prazo: {task['due_date']}\n"

                if task['completed']:
                    result += f"   ✅ Concluída em: {task['completed_at']}\n"

                result += "\n"

            if len(filtered_tasks) > limit:
                result += f"... e mais {len(filtered_tasks) - limit} tarefas"

            return result

        except Exception as e:
            self.logger.error(f"Erro ao listar tarefas: {e}")
            return f"Erro ao listar tarefas: {str(e)}"

    async def complete_task(self, task_id: int) -> str:
        """
        Marca uma tarefa como concluída.

        Args:
            task_id: ID da tarefa

        Returns:
            Confirmação da conclusão
        """
        try:
            task = next((t for t in self.tasks if t['id'] == task_id), None)

            if not task:
                return f"Tarefa #{task_id} não encontrada"

            if task['completed']:
                return f"Tarefa #{task_id} já está concluída"

            task['completed'] = True
            task['completed_at'] = datetime.now().isoformat()

            await self.save_data()

            self.logger.info(f"Tarefa concluída: {task['title']}")
            return f"Tarefa #{task_id} '{task['title']}' marcada como concluída! 🎉"

        except Exception as e:
            self.logger.error(f"Erro ao concluir tarefa: {e}")
            return f"Erro ao concluir tarefa: {str(e)}"

    async def delete_task(self, task_id: int, confirm: bool = False) -> str:
        """
        Deleta uma tarefa.

        Args:
            task_id: ID da tarefa
            confirm: Confirmação de deleção

        Returns:
            Confirmação da deleção
        """
        try:
            if not confirm:
                return f"ATENÇÃO: Deletar tarefa #{task_id} permanentemente? Use confirm=True para confirmar."

            task = next((t for t in self.tasks if t['id'] == task_id), None)

            if not task:
                return f"Tarefa #{task_id} não encontrada"

            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            await self.save_data()

            self.logger.warning(f"Tarefa deletada: {task['title']}")
            return f"Tarefa #{task_id} '{task['title']}' deletada permanentemente"

        except Exception as e:
            self.logger.error(f"Erro ao deletar tarefa: {e}")
            return f"Erro ao deletar tarefa: {str(e)}"

    async def create_note(self, title: str, content: str, tags: str = "") -> str:
        """
        Cria uma nova nota.

        Args:
            title: Título da nota
            content: Conteúdo da nota
            tags: Tags separadas por vírgula

        Returns:
            Confirmação da criação
        """
        try:
            title = validate_string(title, max_length=200)
            content = validate_string(content, max_length=5000)

            tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
            note_id = self.next_note_id
            self.next_note_id += 1

            note = {
                'id': note_id,
                'title': title,
                'content': content,
                'tags': tag_list,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            self.notes.append(note)
            await self.save_data()

            self.logger.info(f"Nota criada: {title}")
            return f"Nota #{note_id} '{title}' criada com sucesso"

        except Exception as e:
            self.logger.error(f"Erro ao criar nota: {e}")
            return f"Erro ao criar nota: {str(e)}"

    async def list_notes(self, limit: int = 10) -> str:
        """
        Lista notas recentes.

        Args:
            limit: Número máximo de notas

        Returns:
            Lista formatada de notas
        """
        try:
            if not self.notes:
                return "Nenhuma nota encontrada"

            # Ordenar por data de criação (mais recentes primeiro)
            sorted_notes = sorted(self.notes, key=lambda x: x['created_at'], reverse=True)

            result = "Notas recentes:\n"
            for note in sorted_notes[:limit]:
                result += f"📝 #{note['id']} {note['title']}\n"
                result += f"   {note['content'][:150]}{'...' if len(note['content']) > 150 else ''}\n"

                if note['tags']:
                    result += f"   🏷️ Tags: {', '.join(note['tags'])}\n"

                result += f"   📅 {note['created_at'][:19].replace('T', ' ')}\n\n"

            if len(self.notes) > limit:
                result += f"... e mais {len(self.notes) - limit} notas"

            return result

        except Exception as e:
            self.logger.error(f"Erro ao listar notas: {e}")
            return f"Erro ao listar notas: {str(e)}"

    async def search_tasks(self, query: str) -> str:
        """
        Busca tarefas por texto.

        Args:
            query: Texto para buscar

        Returns:
            Tarefas encontradas
        """
        try:
            query = query.lower()
            matches = []

            for task in self.tasks:
                if query in task['title'].lower() or query in task['description'].lower():
                    matches.append(task)

            if not matches:
                return f"Nenhuma tarefa encontrada com '{query}'"

            result = f"Tarefas encontradas com '{query}':\n"
            for task in matches:
                status_icon = "✅" if task['completed'] else "⏳"
                result += f"{status_icon} #{task['id']} {task['title']}\n"
                result += f"   {task['description'][:100]}{'...' if len(task['description']) > 100 else ''}\n\n"

            return result

        except Exception as e:
            self.logger.error(f"Erro ao buscar tarefas: {e}")
            return f"Erro na busca: {str(e)}"
