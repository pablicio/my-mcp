#!/usr/bin/env python3
"""
🔧 Script para corrigir o arquivo .env automaticamente
"""

import re
from pathlib import Path

print("="*60)
print("🔧 CORRETOR AUTOMÁTICO DO .ENV")
print("="*60)

env_file = Path(".env")

if not env_file.exists():
    print("\n❌ Arquivo .env não encontrado!")
    print("💡 Copie .env.example para .env primeiro")
    exit(1)

print("\n📄 Lendo arquivo .env...")
with open(env_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("✅ Arquivo lido")

# Contar problemas
original_content = content
problems_found = 0

# Procurar por ALLOWED_DIRECTORIES com barras invertidas
lines = content.split('\n')
new_lines = []

for line in lines:
    if line.strip().startswith('ALLOWED_DIRECTORIES=') and not line.strip().startswith('#'):
        # Extrair o valor
        if '=' in line:
            key, value = line.split('=', 1)
            value = value.strip()
            
            # Verificar se tem barras invertidas
            if '\\' in value:
                print(f"\n⚠️  Problema encontrado:")
                print(f"   Antes: {line}")
                
                # Converter barras invertidas duplas para normais
                value = value.replace('\\\\', '/')
                # Converter barras invertidas simples para normais
                value = value.replace('\\', '/')
                
                new_line = f"{key}={value}"
                print(f"   Depois: {new_line}")
                new_lines.append(new_line)
                problems_found += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

if problems_found > 0:
    print(f"\n🔧 Corrigindo {problems_found} problema(s)...")
    
    # Escrever arquivo corrigido
    new_content = '\n'.join(new_lines)
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Arquivo .env corrigido!")
    
    # Mostrar o que mudou
    print("\n📝 Mudanças:")
    for line in new_lines:
        if 'ALLOWED_DIRECTORIES=' in line and not line.strip().startswith('#'):
            print(f"   {line}")
else:
    print("\n✅ Arquivo .env já está correto!")
    for line in lines:
        if 'ALLOWED_DIRECTORIES=' in line and not line.strip().startswith('#'):
            print(f"   📝 {line}")

print("\n" + "="*60)
print("✅ CORREÇÃO CONCLUÍDA!")
print("="*60)
print("\n💡 Próximo passo: python test_env.py")
