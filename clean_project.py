#!/usr/bin/env python3
"""
🧹 Script de limpeza do projeto MCP Server Pessoal
Remove arquivos temporários, documentação redundante e configurações de debug.
"""

import os
import shutil
from pathlib import Path

# Arquivos MD desnecessários para remover
MD_FILES_TO_REMOVE = [
    "GUIA_COMPLETO.md",
    "QUICK_REFERENCE.md",
    "FAQ.md",
    "COMO_USAR.md",
    "TESTES.md",
    "GUIA_EXECUCAO.md",
    "SUMARIO.md",
    "CORRECAO_ENV.md",
    "CORRECOES_DEPENDENCIAS.md"
]

# Arquivos TXT desnecessários
TXT_FILES_TO_REMOVE = [
    "CORRECAO_DEFINITIVA.txt",
    "CORRECAO_FINAL.txt",
    "RESUMO_COMPLETO.txt",
    "RESUMO_CORRECOES.txt",
    "RESUMO_ENV.txt",
    "STATUS.txt"
]

# Scripts de debug/fix temporários
DEBUG_FILES_TO_REMOVE = [
    "check_env.py",
    "debug_env.py",
    "fix_env.py",
    "test_env.py",
    "test_imports.py",
    "test_settings_simple.py",
    "cleanup_project.py"  # Este próprio script será removido após execução
]

# Arquivos BAT de teste temporários
BAT_FILES_TO_REMOVE = [
    "test_all.bat",
    "test_final.bat",
    "fix_dependencies.bat"
]

# Outros arquivos
OTHER_FILES_TO_REMOVE = [
    "index.html"
]

def remove_files(file_list, description):
    """Remove uma lista de arquivos."""
    print(f"\n📝 Removendo {description}...")
    removed = 0
    for filename in file_list:
        filepath = Path(filename)
        if filepath.exists():
            try:
                filepath.unlink()
                print(f"   ✅ Removido: {filename}")
                removed += 1
            except Exception as e:
                print(f"   ❌ Erro ao remover {filename}: {e}")
        else:
            print(f"   ⏭️  Não encontrado: {filename}")
    return removed

def main():
    """Executa a limpeza do projeto."""
    print("="*60)
    print("🧹 LIMPEZA DO PROJETO MCP SERVER PESSOAL")
    print("="*60)
    print("\nEste script irá remover arquivos desnecessários:")
    print("  - Documentação redundante")
    print("  - Scripts de debug temporários")
    print("  - Arquivos de correção/status temporários")
    print("\n⚠️  ATENÇÃO: Esta ação não pode ser desfeita!")
    
    response = input("\nDeseja continuar? (s/N): ").strip().lower()
    if response != 's':
        print("❌ Operação cancelada.")
        return
    
    total_removed = 0
    
    # Remover cada categoria
    total_removed += remove_files(MD_FILES_TO_REMOVE, "arquivos Markdown desnecessários")
    total_removed += remove_files(TXT_FILES_TO_REMOVE, "arquivos TXT temporários")
    total_removed += remove_files(DEBUG_FILES_TO_REMOVE, "scripts de debug")
    total_removed += remove_files(BAT_FILES_TO_REMOVE, "scripts BAT de teste")
    total_removed += remove_files(OTHER_FILES_TO_REMOVE, "outros arquivos")
    
    print("\n" + "="*60)
    print(f"✅ Limpeza concluída!")
    print(f"📊 Total de arquivos removidos: {total_removed}")
    print("="*60)
    
    print("\n📁 Estrutura limpa mantém:")
    print("   ✅ README.md - Documentação principal")
    print("   ✅ .env / .env.example - Configurações")
    print("   ✅ setup.py - Script de instalação")
    print("   ✅ main.py - Servidor")
    print("   ✅ start.bat / start.sh - Scripts de inicialização")
    print("   ✅ tests/ - Todos os testes centralizados")
    print("   ✅ core/, modules/, config/, utils/ - Código fonte")
    
    print("\n💡 Próximos passos:")
    print("   1. Revise o README.md atualizado")
    print("   2. Execute: python -m tests.quick_test")
    print("   3. Execute: python main.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
