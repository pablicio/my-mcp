"""
Servidor MCP principal.
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
                self.logger.info(f"Carregando modulo {name}...")
                module = module_class()

                if await module.is_available():
                    await module.initialize()
                    self.modules[name] = module
                    self.registry.register_module(name, module)
                    self.logger.info(f"Modulo {name} carregado com sucesso")
                else:
                    self.logger.warning(f"Modulo {name} nao esta disponivel")

            except Exception as e:
                self.logger.error(f"Erro ao carregar modulo {name}: {e}")

    async def register_tools(self):
        """Registra todas as ferramentas no FastMCP."""
        for tool_name, tool_func in self.registry.tools.items():
            # Usar o decorator corretamente com ()
            decorated_tool = self.mcp.tool()(tool_func)
            self.logger.debug(f"Ferramenta registrada: {tool_name}")

    def run_sync(self):
        """Executa o servidor MCP de forma síncrona."""
        try:
            # Inicializar módulos primeiro
            asyncio.run(self.initialize())
            
            self.logger.info("Servidor MCP inicializado com sucesso!")
            self.logger.info("Aguardando conexao do Claude Desktop...")
            self.logger.info("Para parar: Ctrl+C")
            
            # FastMCP.run() gerencia seu próprio loop asyncio
            self.mcp.run()
            
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
