#!/usr/bin/env python3
"""
🧪 Teste rápido do arquivo .env
"""

import sys
from pathlib import Path

print("="*60)
print("🧪 TESTE DE CONFIGURAÇÃO .ENV")
print("="*60)

# Teste 1: Verificar se .env existe
print("\n📄 Teste 1: Arquivo .env...")
env_file = Path(".env")
if env_file.exists():
    print("   ✅ Arquivo .env encontrado")
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
        if "ALLOWED_DIRECTORIES" in content:
            print("   ✅ ALLOWED_DIRECTORIES configurado")
            # Mostrar a linha
            for line in content.split("\n"):
                if "ALLOWED_DIRECTORIES=" in line and not line.strip().startswith("#"):
                    print(f"   📝 {line.strip()}")
        else:
            print("   ⚠️  ALLOWED_DIRECTORIES não encontrado")
else:
    print("   ❌ Arquivo .env não encontrado")
    print("   💡 Copie .env.example para .env")
    sys.exit(1)

# Teste 2: Carregar configurações
print("\n⚙️  Teste 2: Carregando configurações...")
try:
    from config.settings import settings
    print("   ✅ Configurações carregadas com sucesso")
    print(f"   📝 ALLOWED_DIRECTORIES (raw): {repr(settings.ALLOWED_DIRECTORIES)}")
    
    # Obter lista de diretórios
    dirs = settings.get_allowed_directories()
    print(f"   📁 Diretórios permitidos: {len(dirs)}")
    
    if len(dirs) == 0:
        if not settings.ALLOWED_DIRECTORIES:
            print("   ⚠️  Nenhum diretório configurado no .env")
            print("   💡 Adicione diretórios ao .env:")
            print("      ALLOWED_DIRECTORIES=C:/projetos,C:/Users/Usuario/Documents")
        else:
            print("   ⚠️  Diretórios configurados mas inválidos:")
            print(f"      {settings.ALLOWED_DIRECTORIES}")
            print("   💡 Verifique se os caminhos existem")
    else:
        for i, dir_path in enumerate(dirs, 1):
            print(f"   {i}. ✅ {dir_path}")
    
except Exception as e:
    print(f"   ❌ Erro ao carregar: {e}")
    import traceback
    print("\n   Stack trace:")
    traceback.print_exc()
    print("\n💡 Solução:")
    print("   1. Abra o arquivo .env")
    print("   2. Certifique-se que está: ALLOWED_DIRECTORIES=C:/projetos")
    print("   3. Execute: python debug_env.py (para mais detalhes)")
    sys.exit(1)

# Teste 3: Outras configurações
print("\n🔧 Teste 3: Outras configurações...")
try:
    print(f"   📊 Log Level: {settings.LOG_LEVEL}")
    print(f"   🗂️  Tasks DB: {settings.TASKS_DB_PATH}")
    print(f"   🐛 Debug: {settings.DEBUG}")
    print(f"   🔒 Max File Size: {settings.MAX_FILE_SIZE / 1024 / 1024:.1f} MB")
except Exception as e:
    print(f"   ⚠️  Erro: {e}")

print("\n" + "="*60)
print("✅ TESTE CONCLUÍDO!")
print("="*60)
print("\n💡 Próximo passo: python test_server.py")
