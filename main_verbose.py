#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server Pessoal v1.0.0 - MODO VERBOSE
Versão com feedback visual para testes e desenvolvimento.
"""

import logging
import sys
import asyncio
from pathlib import Path
from datetime import datetime
import os

# Adicionar o diretório raiz ao sys.path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.server import MCPPersonalServer
    from config.settings import settings
    from config.logging import setup_logging
except ImportError as e:
    print(f"❌ ERRO de importacao: {e}")
    print("Execute o setup primeiro: python setup.py")
    sys.exit(1)

def print_banner():
    """Imprime banner de inicialização."""
    print("\n" + "="*70)
    print("🚀 MCP SERVER PESSOAL v1.0.0 - MODO VERBOSE")
    print("="*70)
    print(f"📅 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Debug Mode: {'✅ Ativado' if settings.DEBUG else '❌ Desativado'}")
    print(f"📂 Diretórios permitidos: {len(settings.get_allowed_directories())}")
    for i, dir_path in enumerate(settings.get_allowed_directories(), 1):
        print(f"   {i}. {dir_path}")
    print(f"📝 Log File: {settings.LOG_FILE}")
    print(f"📊 Tasks DB: {settings.TASKS_DB_PATH}")
    print("="*70 + "\n")

def print_connection_info():
    """Imprime informações de conexão."""
    print("\n" + "📡 INFORMAÇÕES DE CONEXÃO" + "\n" + "-"*70)
    print("O servidor MCP está rodando e aguardando conexão do Claude Desktop.")
    print("\n💡 COMO VERIFICAR SE ESTÁ CONECTADO:")
    print("   1. Abra o Claude Desktop")
    print("   2. Digite qualquer mensagem")
    print("   3. Verifique o arquivo de log abaixo")
    print(f"   4. Ou use: 'liste minhas tarefas' ou 'crie uma nota'")
    print("\n📁 MONITORAR LOGS EM TEMPO REAL:")
    print(f"   Windows: Get-Content '{settings.LOG_FILE}' -Wait -Tail 20")
    print(f"   Linux/Mac: tail -f {settings.LOG_FILE}")
    print("-"*70 + "\n")

async def check_modules():
    """Verifica e lista módulos disponíveis."""
    print("🔌 VERIFICANDO MÓDULOS...")
    print("-"*70)
    
    server = MCPPersonalServer()
    await server.initialize()
    
    print(f"\n✅ Módulos carregados: {len(server.modules)}")
    for name, module in server.modules.items():
        status = module.get_status()
        print(f"   • {name.upper()}: {status.get('status', 'unknown')}")
        if hasattr(module, 'get_tools'):
            tools = module.get_tools()
            print(f"     Ferramentas: {', '.join([t.__name__ for t in tools])}")
    
    print(f"\n📦 Total de ferramentas registradas: {len(server.registry.tools)}")
    print("-"*70 + "\n")
    
    return server

def main():
    """Função principal para iniciar o servidor MCP em modo verbose."""
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Banner inicial
    print_banner()
    
    try:
        # Verificar módulos
        print("⏳ Inicializando servidor...\n")
        server = asyncio.run(check_modules())
        
        # Informações de conexão
        print_connection_info()
        
        # Avisar que logs não aparecem aqui
        print("⚠️  IMPORTANTE:")
        print("   Logs de operações NÃO aparecem neste terminal!")
        print("   Isso é normal - MCP usa stdout para comunicação.")
        print("   Use o comando acima para monitorar o log em tempo real.\n")
        
        print("✅ Servidor pronto! Aguardando conexão do Claude Desktop...")
        print("   Pressione Ctrl+C para parar\n")
        
        logger.info("="*60)
        logger.info("SERVIDOR INICIADO EM MODO VERBOSE")
        logger.info(f"Módulos: {list(server.modules.keys())}")
        logger.info(f"Ferramentas: {len(server.registry.tools)}")
        logger.info("="*60)
        
        # Executar servidor
        server.mcp.run()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor interrompido pelo usuário")
        logger.info("Servidor interrompido pelo usuario")
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        logger.error(f"Erro fatal: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido")
