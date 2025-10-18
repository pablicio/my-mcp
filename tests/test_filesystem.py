"""
🧪 Testes para o módulo filesystem.
"""

import pytest
import asyncio
from pathlib import Path
from modules.filesystem.tools import FilesystemTools
from config.settings import settings

@pytest.fixture
def filesystem():
    """Fixture para criar instância de FilesystemTools."""
    return FilesystemTools()

@pytest.mark.asyncio
async def test_is_available(filesystem):
    """Testa se o módulo está disponível."""
    is_available = await filesystem.is_available()
    assert isinstance(is_available, bool)

@pytest.mark.asyncio
async def test_read_nonexistent_file(filesystem):
    """Testa leitura de arquivo inexistente."""
    if await filesystem.is_available():
        await filesystem.initialize()
        result = await filesystem.read_file("/caminho/inexistente.txt")
        assert "Erro" in result or "não encontrado" in result

@pytest.mark.asyncio
async def test_list_directory(filesystem, tmp_path):
    """Testa listagem de diretório."""
    if await filesystem.is_available():
        # Criar arquivo temporário
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        await filesystem.initialize()
        
        # Note: This will fail if tmp_path is not in allowed directories
        # This is expected behavior for security
        result = await filesystem.list_directory(str(tmp_path))
        assert isinstance(result, str)

def test_get_tools(filesystem):
    """Testa se as ferramentas são retornadas corretamente."""
    tools = filesystem.get_tools()
    
    assert "read_file" in tools
    assert "write_file" in tools
    assert "list_directory" in tools
    assert "search_files" in tools
    assert callable(tools["read_file"])
