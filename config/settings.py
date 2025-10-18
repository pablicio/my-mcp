"""
⚙️ Configurações do MCP Server Pessoal
Gerenciamento centralizado de todas as configurações usando Pydantic.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configurações do servidor MCP."""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

    # Servidor
    HOST: str = "localhost"
    PORT: int = 8080
    DEBUG: bool = False

    # Google Calendar
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/oauth2callback"

    # Sistema de arquivos
    ALLOWED_DIRECTORIES: str = ""  # Mudado para str, vamos parsear depois
    MAX_FILE_SIZE: int = 10485760  # 10MB

    # Tarefas
    TASKS_DB_PATH: str = "./data/tasks.json"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/mcp_server.log"

    # Segurança
    OPERATION_TIMEOUT: int = 30
    ALLOW_RECURSIVE_ACCESS: bool = True

    @field_validator('ALLOWED_DIRECTORIES', mode='before')
    @classmethod
    def parse_directories(cls, v):
        """Parse directories from string."""
        if v is None or v == "":
            return ""
        if isinstance(v, str):
            # Remove aspas se existirem
            v = v.strip().strip('"').strip("'")
        return v

    @field_validator('LOG_LEVEL', mode='before')
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            print(f"⚠️ Nível de log inválido: {v}. Usando INFO.")
            return 'INFO'
        return v.upper()

    def get_allowed_directories(self) -> List[str]:
        """Retorna lista de diretórios permitidos válidos."""
        if not self.ALLOWED_DIRECTORIES:
            return []
        
        # Parse a string
        dirs = [d.strip() for d in self.ALLOWED_DIRECTORIES.split(',') if d.strip()]
        
        # Valida que existem
        valid_dirs = []
        for dir_path in dirs:
            path = Path(dir_path).resolve()
            if path.exists() and path.is_dir():
                valid_dirs.append(str(path))
            else:
                print(f"⚠️ Diretório não encontrado: {dir_path}")
        
        return valid_dirs

    def ensure_directories(self):
        """Cria diretórios necessários se não existirem."""
        dirs_to_create = [
            Path(self.LOG_FILE).parent,
            Path(self.TASKS_DB_PATH).parent,
        ]

        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)

    @property
    def has_google_credentials(self) -> bool:
        """Verifica se há credenciais do Google configuradas."""
        return bool(self.GOOGLE_CLIENT_ID and self.GOOGLE_CLIENT_SECRET)

# Instância global das configurações
settings = Settings()

# Criar diretórios necessários
settings.ensure_directories()

# Adicionar propriedade dinâmica para compatibilidade
Settings.ALLOWED_DIRECTORIES_LIST = property(lambda self: self.get_allowed_directories())
