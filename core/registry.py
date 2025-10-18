"""
📋 Registro centralizado de ferramentas.
"""

import logging
from typing import Dict, Callable, Any
from modules.base import BaseModule

class ToolRegistry:
    """Registro centralizado para todas as ferramentas."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tools: Dict[str, Callable] = {}
        self.modules: Dict[str, BaseModule] = {}

    def register_module(self, name: str, module: BaseModule):
        """Registra um módulo e suas ferramentas."""
        self.modules[name] = module

        # Registrar todas as ferramentas do módulo
        for tool_name, tool_func in module.get_tools().items():
            self.register_tool(f"{name}_{tool_name}", tool_func)

    def register_tool(self, name: str, func: Callable):
        """Registra uma ferramenta individual."""
        if name in self.tools:
            self.logger.warning(f"Sobrescrevendo ferramenta: {name}")

        self.tools[name] = func
        self.logger.debug(f"Ferramenta registrada: {name}")

    def get_tool(self, name: str) -> Callable:
        """Obtém uma ferramenta pelo nome."""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, str]:
        """Lista todas as ferramentas disponíveis."""
        return {name: func.__doc__ or "Sem descrição" for name, func in self.tools.items()}
