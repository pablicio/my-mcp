"""
📁 Ferramentas de sistema de arquivos com segurança.
"""

import os
import json
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from modules.base import BaseModule
from config.settings import settings
from utils.validators import validate_path
from core.security import is_path_allowed

class FilesystemTools(BaseModule):
    """Módulo de acesso seguro ao sistema de arquivos."""

    def __init__(self):
        super().__init__()
        self.allowed_dirs = []

    async def is_available(self) -> bool:
        """Verifica se há diretórios permitidos configurados."""
        return bool(settings.ALLOWED_DIRECTORIES)

    async def initialize(self):
        """Inicializa e valida os diretórios permitidos."""
        try:
            self.allowed_dirs = settings.get_allowed_directories()
            
            if not self.allowed_dirs:
                raise ValueError("Nenhum diretório válido configurado")
            
            for dir_path in self.allowed_dirs:
                self.logger.info(f"Diretório permitido: {dir_path}")

            self.initialized = True
            self.logger.info(f"Filesystem inicializado com {len(self.allowed_dirs)} diretórios")

        except Exception as e:
            self.logger.error(f"Erro ao inicializar Filesystem: {e}")
            raise

    def get_tools(self) -> Dict[str, callable]:
        """Retorna as ferramentas do filesystem."""
        return {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "list_directory": self.list_directory,
            "search_files": self.search_files,
            "delete_file": self.delete_file,
            "create_directory": self.create_directory,
            "file_info": self.file_info
        }

    async def read_file(self, filepath: str) -> str:
        """
        Lê o conteúdo de um arquivo.

        Args:
            filepath: Caminho para o arquivo

        Returns:
            Conteúdo do arquivo ou mensagem de erro
        """
        try:
            path = validate_path(filepath)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {filepath}"

            if not path.exists():
                return f"Erro: Arquivo não encontrado {filepath}"

            if not path.is_file():
                return f"Erro: Caminho não é um arquivo {filepath}"

            # Verificar tamanho do arquivo (limite de 10MB)
            if path.stat().st_size > settings.MAX_FILE_SIZE:
                return f"Erro: Arquivo muito grande (>10MB) {filepath}"

            async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                content = await f.read()

            self.logger.info(f"Arquivo lido: {filepath}")
            return content

        except UnicodeDecodeError:
            return f"Erro: Arquivo não é texto UTF-8 {filepath}"
        except Exception as e:
            self.logger.error(f"Erro ao ler arquivo {filepath}: {e}")
            return f"Erro ao ler arquivo: {str(e)}"

    async def write_file(self, filepath: str, content: str, overwrite: bool = False) -> str:
        """
        Escreve conteúdo em um arquivo.

        Args:
            filepath: Caminho para o arquivo
            content: Conteúdo a escrever
            overwrite: Se deve sobrescrever arquivo existente

        Returns:
            Mensagem de sucesso ou erro
        """
        try:
            path = validate_path(filepath)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {filepath}"

            if path.exists() and not overwrite:
                return f"Erro: Arquivo já existe, use overwrite=True {filepath}"

            # Criar diretório pai se não existir
            path.parent.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(path, 'w', encoding='utf-8') as f:
                await f.write(content)

            self.logger.info(f"Arquivo escrito: {filepath}")
            return f"Arquivo {filepath} salvo com sucesso ({len(content)} caracteres)"

        except Exception as e:
            self.logger.error(f"Erro ao escrever arquivo {filepath}: {e}")
            return f"Erro ao escrever arquivo: {str(e)}"

    async def list_directory(self, dir_path: str = ".", recursive: bool = False) -> str:
        """
        Lista conteúdo de um diretório.

        Args:
            dir_path: Caminho do diretório
            recursive: Se deve listar recursivamente

        Returns:
            Lista formatada do conteúdo
        """
        try:
            path = validate_path(dir_path)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {dir_path}"

            if not path.exists():
                return f"Erro: Diretório não encontrado {dir_path}"

            if not path.is_dir():
                return f"Erro: Caminho não é um diretório {dir_path}"

            items = []

            if recursive:
                for item in path.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(path)
                        size = item.stat().st_size
                        items.append(f"📄 {rel_path} ({size} bytes)")
                    elif item.is_dir():
                        rel_path = item.relative_to(path)
                        items.append(f"📁 {rel_path}/")
            else:
                for item in sorted(path.iterdir()):
                    if item.is_file():
                        size = item.stat().st_size
                        items.append(f"📄 {item.name} ({size} bytes)")
                    elif item.is_dir():
                        items.append(f"📁 {item.name}/")

            if not items:
                return f"Diretório vazio: {dir_path}"

            result = f"Conteúdo de {dir_path}:\n"
            result += "\n".join(items[:100])  # Limitar a 100 itens

            if len(items) > 100:
                result += f"\n... e mais {len(items) - 100} itens"

            return result

        except Exception as e:
            self.logger.error(f"Erro ao listar diretório {dir_path}: {e}")
            return f"Erro ao listar diretório: {str(e)}"

    async def search_files(self, pattern: str, dir_path: str = ".", max_results: int = 50) -> str:
        """
        Busca arquivos por padrão de nome.

        Args:
            pattern: Padrão de busca (suporta wildcards)
            dir_path: Diretório para buscar
            max_results: Máximo de resultados

        Returns:
            Lista de arquivos encontrados
        """
        try:
            path = validate_path(dir_path)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {dir_path}"

            if not path.exists() or not path.is_dir():
                return f"Erro: Diretório inválido {dir_path}"

            matches = list(path.rglob(pattern))[:max_results]

            if not matches:
                return f"Nenhum arquivo encontrado com padrão '{pattern}' em {dir_path}"

            result = f"Arquivos encontrados com padrão '{pattern}':\n"
            for match in matches:
                if match.is_file():
                    rel_path = match.relative_to(path)
                    size = match.stat().st_size
                    result += f"📄 {rel_path} ({size} bytes)\n"
                elif match.is_dir():
                    rel_path = match.relative_to(path)
                    result += f"📁 {rel_path}/\n"

            if len(matches) == max_results:
                result += f"\nMostrando primeiros {max_results} resultados"

            return result

        except Exception as e:
            self.logger.error(f"Erro ao buscar arquivos: {e}")
            return f"Erro na busca: {str(e)}"

    async def file_info(self, filepath: str) -> str:
        """
        Obtém informações detalhadas sobre um arquivo.

        Args:
            filepath: Caminho do arquivo

        Returns:
            Informações formatadas do arquivo
        """
        try:
            path = validate_path(filepath)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {filepath}"

            if not path.exists():
                return f"Erro: Arquivo não encontrado {filepath}"

            stat = path.stat()

            info = f"Informações de {filepath}:\n"
            info += f"Tipo: {'Arquivo' if path.is_file() else 'Diretório' if path.is_dir() else 'Outro'}\n"
            info += f"Tamanho: {stat.st_size:,} bytes\n"
            info += f"Modificado: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            info += f"Criado: {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            info += f"Permissões: {oct(stat.st_mode)[-3:]}\n"

            if path.is_file():
                # Detectar tipo de arquivo pela extensão
                suffix = path.suffix.lower()
                file_types = {
                    '.txt': 'Texto', '.md': 'Markdown', '.py': 'Python', 
                    '.js': 'JavaScript', '.json': 'JSON', '.csv': 'CSV', '.pdf': 'PDF'
                }
                file_type = file_types.get(suffix, 'Desconhecido')
                info += f"Tipo de arquivo: {file_type}\n"

            return info

        except Exception as e:
            self.logger.error(f"Erro ao obter info do arquivo {filepath}: {e}")
            return f"Erro ao obter informações: {str(e)}"

    async def delete_file(self, filepath: str, confirm: bool = False) -> str:
        """Deleta um arquivo com confirmação."""
        try:
            if not confirm:
                return f"ATENÇÃO: Deletar '{filepath}' permanentemente? Use confirm=True para confirmar."

            path = validate_path(filepath)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {filepath}"

            if not path.exists():
                return f"Erro: Arquivo não encontrado {filepath}"

            if path.is_file():
                path.unlink()
                self.logger.warning(f"Arquivo deletado: {filepath}")
                return f"Arquivo {filepath} deletado com sucesso"
            else:
                return f"Erro: Use ferramenta específica para deletar diretórios {filepath}"

        except Exception as e:
            self.logger.error(f"Erro ao deletar arquivo {filepath}: {e}")
            return f"Erro ao deletar arquivo: {str(e)}"

    async def create_directory(self, dir_path: str) -> str:
        """Cria um novo diretório."""
        try:
            path = validate_path(dir_path)

            if not is_path_allowed(path, self.allowed_dirs):
                return f"Erro: Acesso negado ao caminho {dir_path}"

            path.mkdir(parents=True, exist_ok=False)
            self.logger.info(f"Diretório criado: {dir_path}")
            return f"Diretório {dir_path} criado com sucesso"

        except FileExistsError:
            return f"Erro: Diretório já existe {dir_path}"
        except Exception as e:
            self.logger.error(f"Erro ao criar diretório {dir_path}: {e}")
            return f"Erro ao criar diretório: {str(e)}"
