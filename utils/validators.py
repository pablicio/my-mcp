"""
🔧 Utilitários de validação.
"""

from pathlib import Path
from typing import Union

def validate_path(path_str: Union[str, Path]) -> Path:
    """
    Valida e normaliza um caminho de arquivo/diretório.
    
    Args:
        path_str: Caminho como string ou Path
        
    Returns:
        Path normalizado
        
    Raises:
        ValueError: Se o caminho é inválido ou perigoso
    """
    try:
        # Converter para Path
        path = Path(path_str)
        
        # Resolver para caminho absoluto
        path = path.resolve()
        
        # Verificar tentativas de path traversal
        path_str_normalized = str(path).replace('\\', '/')
        if '..' in path.parts or '../' in path_str_normalized or '..\\' in str(path):
            raise ValueError("Path traversal não permitido")
        
        return path
        
    except Exception as e:
        raise ValueError(f"Caminho inválido: {e}")

def validate_filename(filename: str) -> str:
    """
    Valida um nome de arquivo.
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        Nome validado
        
    Raises:
        ValueError: Se o nome é inválido
    """
    if not filename or not filename.strip():
        raise ValueError("Nome de arquivo vazio")
    
    # Caracteres proibidos
    forbidden = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']
    
    for char in forbidden:
        if char in filename:
            raise ValueError(f"Caractere proibido no nome: {char}")
    
    # Nomes reservados no Windows
    reserved = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    
    if filename.upper() in reserved:
        raise ValueError(f"Nome reservado do sistema: {filename}")
    
    return filename.strip()

def validate_string(text: str, min_length: int = 1, max_length: int = 1000) -> str:
    """
    Valida uma string de entrada.
    
    Args:
        text: Texto a validar
        min_length: Comprimento mínimo
        max_length: Comprimento máximo
        
    Returns:
        String validada e limpa
        
    Raises:
        ValueError: Se a string é inválida
    """
    if not isinstance(text, str):
        raise ValueError("Entrada deve ser uma string")
    
    text = text.strip()
    
    if len(text) < min_length:
        raise ValueError(f"Texto muito curto (mínimo {min_length} caracteres)")
    
    if len(text) > max_length:
        raise ValueError(f"Texto muito longo (máximo {max_length} caracteres)")
    
    return text
