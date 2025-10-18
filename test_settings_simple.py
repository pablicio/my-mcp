#!/usr/bin/env python3
"""
🧪 Teste simples de importação do settings
"""

import sys
import traceback

print("="*60)
print("🧪 TESTE SIMPLES DE SETTINGS")
print("="*60)

print("\n1️⃣ Importando settings...")
try:
    from config.settings import settings
    print("✅ Settings importado com sucesso!")
    print(f"   ALLOWED_DIRECTORIES (raw): {repr(settings.ALLOWED_DIRECTORIES)}")
    
    print("\n2️⃣ Obtendo diretórios...")
    dirs = settings.get_allowed_directories()
    print(f"✅ Diretórios obtidos: {len(dirs)}")
    for i, d in enumerate(dirs, 1):
        print(f"   {i}. {d}")
    
    print("\n3️⃣ Outras configs...")
    print(f"   LOG_LEVEL: {settings.LOG_LEVEL}")
    print(f"   DEBUG: {settings.DEBUG}")
    
    print("\n" + "="*60)
    print("✅ TESTE PASSOU!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\nStack trace completo:")
    traceback.print_exc()
    sys.exit(1)
