"""
🏗️ Classe base para todos os módulos.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Callable, Any

class BaseModule(ABC):
    """Classe base para módulos do servidor MCP."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initialized = False

    @abstractmethod
    async def is_available(self) -> bool:
        """Verifica se o módulo está disponível para uso."""
        pass

    @abstractmethod
    async def initialize(self):
        """Inicializa o módulo."""
        pass

    @abstractmethod
    def get_tools(self) -> Dict[str, Callable]:
        """Retorna as ferramentas disponíveis no módulo."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Retorna o status do módulo."""
        return {
            "initialized": self.initialized,
            "available": True
        }

    async def cleanup(self):
        """Limpa recursos do módulo."""
        self.logger.info(f"Limpando módulo {self.__class__.__name__}")
