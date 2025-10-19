#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scripts de Teste do MCP Server
Acesso rápido aos testes organizados
"""

import sys
import subprocess
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_unit_tests():
    """Executa testes unitários"""
    print("🧪 Executando testes unitários...")
    subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/unit/",
        "-v",
        "--tb=short",
        "--color=yes"
    ])

def run_integration_tests():
    """Executa testes de integração"""
    print("🔗 Executando testes de integração...")
    print("⚠️  Certifique-se de que o servidor está rodando!")
    subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/integration/",
        "-v",
        "--tb=short",
        "--color=yes"
    ])

def run_mcp_tests():
    """Executa testes MCP/Claude"""
    print("📡 Executando testes de conexão MCP...")
    subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/mcp/",
        "-v",
        "--tb=short",
        "--color=yes"
    ])

def run_all_tests():
    """Executa todos os testes"""
    print("="*60)
    print("🚀 EXECUTANDO TODOS OS TESTES")
    print("="*60)
    
    run_unit_tests()
    print()
    run_mcp_tests()
    print()
    run_integration_tests()
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS")
    print("="*60)

def main():
    """Menu principal"""
    print("="*60)
    print("🧪 MCP SERVER - SUITE DE TESTES")
    print("="*60)
    print()
    print("Escolha uma opção:")
    print("  1 - Testes Unitários")
    print("  2 - Testes de Integração (API)")
    print("  3 - Testes MCP/Claude")
    print("  4 - Todos os Testes")
    print("  0 - Sair")
    print()
    
    choice = input("Opção: ").strip()
    
    if choice == "1":
        run_unit_tests()
    elif choice == "2":
        run_integration_tests()
    elif choice == "3":
        run_mcp_tests()
    elif choice == "4":
        run_all_tests()
    elif choice == "0":
        print("Saindo...")
    else:
        print("Opção inválida!")

if __name__ == '__main__':
    main()
