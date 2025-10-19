"""
🧪 Testes para módulo de segurança.
"""

import pytest
from pathlib import Path
from core.security import is_path_allowed, sanitize_filename, is_safe_content

def test_is_path_allowed():
    """Testa validação de caminhos permitidos."""
    allowed_dirs = ["/home/user/docs", "C:\\Users\\User\\Documents"]
    
    # Caminho permitido
    path1 = Path("/home/user/docs/file.txt")
    assert is_path_allowed(path1, ["/home/user/docs"])
    
    # Caminho não permitido
    path2 = Path("/etc/passwd")
    assert not is_path_allowed(path2, allowed_dirs)

def test_sanitize_filename():
    """Testa sanitização de nomes de arquivos."""
    # Nome válido
    assert sanitize_filename("document.txt") == "document.txt"
    
    # Nome com caracteres inválidos
    result = sanitize_filename("file<>:name.txt")
    assert "<" not in result
    assert ">" not in result
    assert ":" not in result
    
    # Nome muito longo
    long_name = "a" * 300 + ".txt"
    result = sanitize_filename(long_name)
    assert len(result) <= 255

def test_is_safe_content():
    """Testa detecção de conteúdo perigoso."""
    # Conteúdo seguro
    assert is_safe_content("Hello, world!")
    assert is_safe_content("# Python comment\nprint('Hello')")
    
    # Conteúdo perigoso
    assert not is_safe_content("<script>alert('xss')</script>")
    assert not is_safe_content("javascript:void(0)")
    assert not is_safe_content("eval(malicious_code)")
    assert not is_safe_content("import os; os.system('rm -rf /')")
