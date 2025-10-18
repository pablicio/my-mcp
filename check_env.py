#!/usr/bin/env python3
"""
✅ Verificação final do .env
"""

print("🔍 Verificando arquivo .env...")
print()

with open(".env", "r", encoding="utf-8") as f:
    for line in f:
        if "ALLOWED_DIRECTORIES=" in line and not line.strip().startswith("#"):
            print(f"Encontrado: {line.strip()}")
            
            if "\\" in line:
                print("❌ AINDA TEM BARRAS INVERTIDAS!")
                print("Execute: python fix_env.py")
            else:
                print("✅ Formato correto!")
                print()
                print("Execute agora: python test_env.py")
            break
