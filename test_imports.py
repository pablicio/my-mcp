#!/usr/bin/env python3
"""
🧪 Teste rápido de importações
"""

import sys

print("="*60)
print("🧪 TESTE DE IMPORTAÇÕES")
print("="*60)

# Teste 1: Pydantic Settings
print("\n📦 Teste 1: pydantic-settings...")
try:
    from pydantic_settings import BaseSettings
    print("   ✅ pydantic-settings importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro: {e}")
    print("   💡 Execute: pip install pydantic-settings")
    sys.exit(1)

# Teste 2: Config Settings
print("\n⚙️  Teste 2: config.settings...")
try:
    from config.settings import settings
    print("   ✅ settings importado com sucesso")
    print(f"   📁 Diretórios: {len(settings.ALLOWED_DIRECTORIES)}")
except ImportError as e:
    print(f"   ❌ Erro: {e}")
    sys.exit(1)

# Teste 3: Core Server
print("\n🚀 Teste 3: core.server...")
try:
    from core.server import MCPPersonalServer
    print("   ✅ MCPPersonalServer importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro: {e}")
    sys.exit(1)

# Teste 4: Módulos
print("\n🔧 Teste 4: módulos...")
try:
    from modules.filesystem.tools import FilesystemTools
    from modules.tasks.tools import TasksTools
    print("   ✅ FilesystemTools importado")
    print("   ✅ TasksTools importado")
except ImportError as e:
    print(f"   ❌ Erro: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ TODOS OS TESTES DE IMPORTAÇÃO PASSARAM!")
print("="*60)
print("\n🎉 As correções funcionaram!")
print("💡 Próximo passo: python test_server.py")
