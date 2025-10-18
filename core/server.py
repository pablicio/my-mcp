"""
🚀 Servidor MCP principal.
"""

import asyncio
import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

from config.settings import settings
from core.registry import ToolRegistry
from modules.calendar.tools import CalendarTools
from modules.filesystem.tools import FilesystemTools  
from modules.tasks.tools import TasksTools

class MCPPersonalServer:
    """Servidor MCP pessoal extensível."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mcp = FastMCP("personal-server")
        self.registry = ToolRegistry()
        self.modules = {}

    async def initialize(self):
        """Inicializa o servidor e todos os módulos."""
        self.logger.info("Inicializando servidor MCP...")

        # Carregar módulos
        await self.load_modules()

        # Registrar ferramentas no MCP
        await self.register_tools()

        self.logger.info(f"Servidor inicializado com {len(self.registry.tools)} ferramentas")

    async def load_modules(self):
        """Carrega todos os módulos disponíveis."""
        modules_to_load = [
            ("calendar", CalendarTools),
            ("filesystem", FilesystemTools), 
            ("tasks", TasksTools)
        ]

        for name, module_class in modules_to_load:
            try:
                self.logger.info(f"Carregando módulo {name}...")
                module = module_class()

                if await module.is_available():
                    await module.initialize()
                    self.modules[name] = module
                    self.registry.register_module(name, module)
                    self.logger.info(f"Módulo {name} carregado com sucesso")
                else:
                    self.logger.warning(f"Módulo {name} não está disponível")

            except Exception as e:
                self.logger.error(f"Erro ao carregar módulo {name}: {e}")

    async def register_tools(self):
        """Registra todas as ferramentas no FastMCP."""
        for tool_name, tool_func in self.registry.tools.items():
            self.mcp.tool(tool_func)
            self.logger.debug(f"Ferramenta registrada: {tool_name}")

    async def run(self):
        """Executa o servidor MCP."""
        try:
            await self.mcp.run(host=settings.HOST, port=settings.PORT)
        except Exception as e:
            self.logger.error(f"Erro ao executar servidor: {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Retorna o status do servidor."""
        return {
            "status": "running",
            "modules": {name: module.get_status() for name, module in self.modules.items()},
            "tools_count": len(self.registry.tools)
        }
