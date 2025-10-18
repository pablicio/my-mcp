#!/usr/bin/env python3
"""
🔍 Debug detalhado do problema do .env
"""

import sys
import traceback
from pathlib import Path

print("="*60)
print("🔍 DEBUG DO PROBLEMA DO .ENV")
print("="*60)

# Teste 1: Ler .env diretamente
print("\n📄 Teste 1: Lendo .env diretamente...")
with open(".env", "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        if "ALLOWED_DIRECTORIES=" in line and not line.strip().startswith("#"):
            print(f"   Linha {line_num}: {repr(line.strip())}")
            print(f"   Comprimento: {len(line.strip())}")
            print(f"   Bytes: {line.strip().encode('utf-8')}")

# Teste 2: python-dotenv
print("\n📦 Teste 2: Testando python-dotenv...")
try:
    from dotenv import dotenv_values
    env_vars = dotenv_values(".env")
    if 'ALLOWED_DIRECTORIES' in env_vars:
        value = env_vars['ALLOWED_DIRECTORIES']
        print(f"   ✅ python-dotenv leu: {repr(value)}")
        print(f"   Tipo: {type(value)}")
    else:
        print("   ⚠️ ALLOWED_DIRECTORIES não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 3: Pydantic BaseSettings sem validadores
print("\n🔧 Teste 3: Pydantic BaseSettings puro...")
try:
    from pydantic import Field
    from pydantic_settings import BaseSettings
    
    class SimpleSettings(BaseSettings):
        ALLOWED_DIRECTORIES: str = ""
        
        class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'
    
    simple = SimpleSettings()
    print(f"   ✅ Pydantic leu: {repr(simple.ALLOWED_DIRECTORIES)}")
    print(f"   Tipo: {type(simple.ALLOWED_DIRECTORIES)}")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    traceback.print_exc()

# Teste 4: Com List[str]
print("\n📋 Teste 4: Pydantic com List[str]...")
try:
    from typing import List
    from pydantic import Field
    from pydantic_settings import BaseSettings
    
    class ListSettings(BaseSettings):
        ALLOWED_DIRECTORIES: List[str] = []
        
        class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'
    
    list_settings = ListSettings()
    print(f"   ✅ Pydantic leu: {repr(list_settings.ALLOWED_DIRECTORIES)}")
    print(f"   Tipo: {type(list_settings.ALLOWED_DIRECTORIES)}")
except Exception as e:
    print(f"   ❌ Erro ao usar List[str]: {e}")
    print("\n   Stack trace completo:")
    traceback.print_exc()

# Teste 5: Nossa classe Settings
print("\n⚙️  Teste 5: Testando config.settings...")
try:
    from config.settings import Settings
    
    # Tentar criar sem .env primeiro
    import os
    backup = os.environ.get('ALLOWED_DIRECTORIES')
    os.environ['ALLOWED_DIRECTORIES'] = 'C:/projetos'
    
    settings_test = Settings()
    print(f"   ✅ Settings criado com env var")
    print(f"   Diretórios: {settings_test.ALLOWED_DIRECTORIES}")
    
    if backup:
        os.environ['ALLOWED_DIRECTORIES'] = backup
    else:
        os.environ.pop('ALLOWED_DIRECTORIES', None)
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
    print("\n   Stack trace completo:")
    traceback.print_exc()

print("\n" + "="*60)
print("🔍 DEBUG CONCLUÍDO")
print("="*60)
