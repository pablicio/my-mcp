"""
Configuração de logging para o servidor MCP.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from config.settings import settings

def setup_logging():
    """Configura o sistema de logging."""
    # Criar formatador
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Limpar handlers existentes
    root_logger.handlers.clear()

    # IMPORTANTE: NÃO logar no console/stdout porque o MCP usa stdout
    # para comunicação com Claude Desktop
    
    # Handler para arquivo (rotativo) com UTF-8
    if settings.LOG_FILE:
        try:
            # Garantir que o diretório existe
            Path(settings.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
            root_logger.addHandler(file_handler)
        except Exception as e:
            # Logar em stderr (não stdout)
            print(f"Aviso: Nao foi possivel configurar log em arquivo: {e}", file=sys.stderr)

    # Handler para stderr (apenas erros críticos)
    if settings.DEBUG:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(formatter)
        stderr_handler.setLevel(logging.ERROR)
        root_logger.addHandler(stderr_handler)

    # Configurar loggers específicos para serem menos verbosos
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
