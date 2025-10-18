#!/usr/bin/env python3
"""
🚀 MCP Server Pessoal v1.0.0
Servidor extensível baseado no Model Context Protocol para uso pessoal.
"""

import asyncio
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
    print(f"❌ Erro de importação: {e}")
    print("💡 Execute o setup primeiro: python setup.py")
    sys.exit(1)

async def main():
    """Função principal para iniciar o servidor MCP."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("="*60)
    logger.info("🚀 MCP SERVER PESSOAL v1.0.0")
    logger.info("="*60)
    logger.info(f"🌐 Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"🐛 Debug: {'Enabled' if settings.DEBUG else 'Disabled'}")

    try:
        server = MCPPersonalServer()
        await server.initialize()

        logger.info("✅ Servidor MCP inicializado com sucesso!")
        logger.info("🔧 Para parar: Ctrl+C")
        logger.info("📊 Logs: ./logs/mcp_server.log")

        await server.run()

    except KeyboardInterrupt:
        logger.info("⏹️ Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        sys.exit(1)
    finally:
        logger.info("🛑 Servidor finalizado")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Servidor interrompido")
