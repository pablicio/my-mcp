#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server Pessoal v1.0.0
Servidor extensível baseado no Model Context Protocol para uso pessoal.
"""

import logging
import sys
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.server import MCPPersonalServer
    from config.settings import settings
    from config.logging import setup_logging
except ImportError as e:
    print(f"ERRO de importacao: {e}")
    print("Execute o setup primeiro: python setup.py")
    sys.exit(1)

def main():
    """Função principal para iniciar o servidor MCP."""
    # Configurar logging para arquivo, não para stdout
    # (stdout é usado para comunicação MCP)
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("="*60)
    logger.info("MCP SERVER PESSOAL v1.0.0")
    logger.info("="*60)
    logger.info(f"Debug: {'Enabled' if settings.DEBUG else 'Disabled'}")
    logger.info(f"Diretorios permitidos: {len(settings.get_allowed_directories())}")

    try:
        server = MCPPersonalServer()
        
        logger.info("Inicializando servidor...")
        server.run_sync()
        
    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuario")
    except Exception as e:
        logger.error(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor interrompido", file=sys.stderr)