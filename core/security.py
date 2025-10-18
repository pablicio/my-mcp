"""
🔒 Validações de segurança para o servidor MCP.
"""

import os
from pathlib import Path
from typing import List

def is_path_allowed(path: Path, allowed_dirs: List[str]) -> bool:
    """
    Verifica se um caminho está dentro dos diretórios permitidos.

    Args:
        path: Caminho a verificar
        allowed_dirs: Lista de diretórios permitidos

    Returns:
        True se o caminho é permitido
    """
    try:
        # Resolver o caminho absoluto
        abs_path = path.resolve()

        # Verificar se está dentro de algum diretório permitido
        for allowed_dir in allowed_dirs:
            allowed_path = Path(allowed_dir).resolve()
            try:
                abs_path.relative_to(allowed_path)
                return True
            except ValueError:
                continue

        return False
    except Exception:
        return False

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza um nome de arquivo removendo caracteres perigosos.

    Args:
        filename: Nome do arquivo

    Returns:
        Nome sanitizado
    """
    # Caracteres não permitidos
    forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']

    for char in forbidden_chars:
        filename = filename.replace(char, '_')

    # Remover espaços extras e pontos no início/fim
    filename = filename.strip('. ')

    # Limitar tamanho
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext

    return filename

def is_safe_content(content: str) -> bool:
    """
    Verifica se o conteúdo é seguro (sem scripts maliciosos).

    Args:
        content: Conteúdo a verificar

    Returns:
        True se o conteúdo é seguro
    """
    # Lista básica de padrões suspeitos
    dangerous_patterns = [
        '<script', 'javascript:', 'data:text/html',
        'eval(', 'import ', 'exec(', 'subprocess.',
        'os.system'
    ]

    content_lower = content.lower()

    for pattern in dangerous_patterns:
        if pattern in content_lower:
            return False

    return True
