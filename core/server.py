"""
Servidor MCP principal.
"""

import asyncio
import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

from config.settings import settings
from core.registry import ToolRegistry
from core.connection_monitor import get_connection_monitor
from modules.calendar.tools import CalendarTools
from modules.filesystem.tools import FilesystemTools  
from modules.tasks.tools import TasksTools
from modules.connections.tools import ConnectionTools

class MCPPersonalServer:
    """Servidor MCP pessoal extensível."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mcp = FastMCP("personal-server")
        self.registry = ToolRegistry()
        self.modules = {}
        self.connection_monitor = get_connection_monitor()
        
        # Registrar servidor como cliente "principal"
        self.connection_monitor.register_client(
            client_id="mcp-server",
            client_name="MCP Personal Server"
        )
        
        # Variável para armazenar ID do cliente atual
        self.current_client_id = "claude-desktop"

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
            ("tasks", TasksTools),
            ("connections", ConnectionTools)
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
            # Criar wrapper para monitoramento com closure correto
            def create_monitored_wrapper(name, func):
                # Preservar a assinatura original da função
                import inspect
                sig = inspect.signature(func)
                
                async def monitored_tool(**kwargs):
                    # Registrar atividade do cliente atual
                    self.connection_monitor.record_activity(
                        client_id=self.current_client_id,
                        tool_name=name
                    )
                    self.logger.info(f"Ferramenta '{name}' chamada por {self.current_client_id} com: {kwargs}")
                    # Executar ferramenta original com os parâmetros corretos
                    return await func(**kwargs)
                
                # Preservar metadados da função original
                monitored_tool.__name__ = func.__name__
                monitored_tool.__doc__ = func.__doc__
                monitored_tool.__annotations__ = func.__annotations__
                monitored_tool.__signature__ = sig
                    
                return monitored_tool
            
            # Criar wrapper monitorado e decorar
            wrapped_func = create_monitored_wrapper(tool_name, tool_func)
            decorated_tool = self.mcp.tool()(wrapped_func)
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
        connection_stats = self.connection_monitor.get_stats()
        
        return {
            "status": "running",
            "modules": {name: module.get_status() for name, module in self.modules.items()},
            "tools_count": len(self.registry.tools),
            "connections": connection_stats,
            "active_clients": len(self.connection_monitor.get_active_clients())
        }
