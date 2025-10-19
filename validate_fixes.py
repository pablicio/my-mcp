#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validação Final
Verifica se todas as correções foram aplicadas corretamente
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_check(passed: bool, message: str):
    status = f"{Colors.GREEN}✅" if passed else f"{Colors.RED}❌"
    print(f"{status} {message}{Colors.END}")

def check_file_exists(path: str) -> bool:
    """Verifica se arquivo existe"""
    return Path(path).exists()

def validate_structure() -> List[Tuple[bool, str]]:
    """Valida estrutura de arquivos"""
    checks = []
    
    # Arquivos principais
    checks.append((
        check_file_exists("core/connection_monitor.py"),
        "Arquivo connection_monitor.py criado"
    ))
    
    # Testes organizados
    checks.append((
        check_file_exists("tests/mcp/test_claude_connection.py"),
        "Testes MCP criados"
    ))
    
    checks.append((
        check_file_exists("tests/integration/test_api_endpoints.py"),
        "Testes de integração organizados"
    ))
    
    checks.append((
        check_file_exists("tests/run_tests.py"),
        "Script de execução de testes criado"
    ))
    
    checks.append((
        check_file_exists("pytest.ini"),
        "Configuração pytest criada"
    ))
    
    checks.append((
        check_file_exists("tests/README.md"),
        "Documentação de testes criada"
    ))
    
    # Scripts batch
    checks.append((
        check_file_exists("tests/run_all_tests.bat"),
        "Scripts batch criados"
    ))
    
    # Documentação
    checks.append((
        check_file_exists("CHANGELOG_FIXES.md"),
        "Changelog de correções criado"
    ))
    
    return checks

def validate_code_changes() -> List[Tuple[bool, str]]:
    """Valida mudanças no código"""
    checks = []
    
    # Verificar importações em api_server.py
    try:
        with open("api_server.py", 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append((
                "from core.connection_monitor import get_connection_monitor" in content,
                "Import connection_monitor em api_server.py"
            ))
            checks.append((
                "def get_connections():" in content,
                "Endpoint /api/connections implementado"
            ))
            checks.append((
                "connection_monitor = None" in content,
                "Variável global connection_monitor definida"
            ))
    except:
        checks.append((False, "Erro ao ler api_server.py"))
    
    # Verificar mudanças em core/server.py
    try:
        with open("core/server.py", 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append((
                "from core.connection_monitor import get_connection_monitor" in content,
                "Import connection_monitor em server.py"
            ))
            checks.append((
                "self.connection_monitor = get_connection_monitor()" in content,
                "Monitor de conexões inicializado em server"
            ))
    except:
        checks.append((False, "Erro ao ler server.py"))
    
    # Verificar mudanças em index.html
    try:
        with open("index.html", 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append((
                'data-tab="connections"' in content,
                "Aba de conexões adicionada ao HTML"
            ))
            checks.append((
                'id="connectionsList"' in content,
                "Container de conexões presente"
            ))
    except:
        checks.append((False, "Erro ao ler index.html"))
    
    # Verificar mudanças em app.js
    try:
        with open("app.js", 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append((
                "loadConnections" in content,
                "Função loadConnections implementada"
            ))
            checks.append((
                "renderConnections" in content,
                "Função renderConnections implementada"
            ))
    except:
        checks.append((False, "Erro ao ler app.js"))
    
    # Verificar mudanças em styles.css
    try:
        with open("styles.css", 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append((
                ".connection-grid" in content,
                "Estilos de conexões adicionados ao CSS"
            ))
            checks.append((
                ".connection-item" in content,
                "Estilos de itens de conexão presentes"
            ))
    except:
        checks.append((False, "Erro ao ler styles.css"))
    
    return checks

def validate_tests() -> List[Tuple[bool, str]]:
    """Valida arquivos de teste"""
    checks = []
    
    # Verificar conteúdo do teste MCP
    try:
        with open("tests/mcp/test_claude_connection.py", 'r', encoding='utf-8') as f:
            content = f.read()
            checks.append((
                "TestClaudeConnection" in content,
                "Classe de teste MCP presente"
            ))
            checks.append((
                "test_server_initialization" in content,
                "Teste de inicialização presente"
            ))
            checks.append((
                "test_create_task_via_mcp" in content,
                "Teste de criação de tarefa via MCP"
            ))
            checks.append((
                "@pytest.mark.asyncio" in content,
                "Suporte a testes assíncronos"
            ))
    except:
        checks.append((False, "Erro ao validar testes MCP"))
    
    # Verificar organização
    checks.append((
        not check_file_exists("test_api.py"),
        "Arquivo test_api.py movido da raiz"
    ))
    
    checks.append((
        not check_file_exists("test_api_complete.py"),
        "Arquivo test_api_complete.py movido da raiz"
    ))
    
    return checks

def count_checks(checks: List[Tuple[bool, str]]) -> Tuple[int, int]:
    """Conta checks passados e falhados"""
    passed = sum(1 for c, _ in checks if c)
    total = len(checks)
    return passed, total

def main():
    """Executa validação completa"""
    print_header("🔍 VALIDAÇÃO DE CORREÇÕES E MELHORIAS")
    print("Verificando se todas as mudanças foram aplicadas corretamente...\n")
    
    # 1. Validar estrutura
    print_header("📁 Estrutura de Arquivos")
    structure_checks = validate_structure()
    for passed, message in structure_checks:
        print_check(passed, message)
    passed_struct, total_struct = count_checks(structure_checks)
    print(f"\n{Colors.BLUE}Estrutura: {passed_struct}/{total_struct} checks passaram{Colors.END}")
    
    # 2. Validar mudanças no código
    print_header("💻 Mudanças no Código")
    code_checks = validate_code_changes()
    for passed, message in code_checks:
        print_check(passed, message)
    passed_code, total_code = count_checks(code_checks)
    print(f"\n{Colors.BLUE}Código: {passed_code}/{total_code} checks passaram{Colors.END}")
    
    # 3. Validar testes
    print_header("🧪 Testes")
    test_checks = validate_tests()
    for passed, message in test_checks:
        print_check(passed, message)
    passed_tests, total_tests = count_checks(test_checks)
    print(f"\n{Colors.BLUE}Testes: {passed_tests}/{total_tests} checks passaram{Colors.END}")
    
    # 4. Resumo final
    print_header("📊 RESUMO FINAL")
    
    total_passed = passed_struct + passed_code + passed_tests
    total_checks = total_struct + total_code + total_tests
    percentage = (total_passed / total_checks * 100) if total_checks > 0 else 0
    
    print(f"Total de checks: {total_checks}")
    print(f"Passaram: {Colors.GREEN}{total_passed}{Colors.END}")
    print(f"Falharam: {Colors.RED}{total_checks - total_passed}{Colors.END}")
    print(f"Percentual: {Colors.GREEN if percentage >= 90 else Colors.YELLOW}{percentage:.1f}%{Colors.END}")
    
    print()
    if percentage == 100:
        print(f"{Colors.GREEN}🎉 TODAS AS CORREÇÕES FORAM APLICADAS COM SUCESSO!{Colors.END}")
        print(f"{Colors.GREEN}✅ Sistema pronto para uso{Colors.END}")
    elif percentage >= 90:
        print(f"{Colors.YELLOW}⚠️  Quase lá! Algumas correções menores faltando{Colors.END}")
        print(f"{Colors.YELLOW}Revise os itens marcados com ❌{Colors.END}")
    else:
        print(f"{Colors.RED}❌ Algumas correções não foram aplicadas{Colors.END}")
        print(f"{Colors.RED}Revise todos os itens marcados com ❌{Colors.END}")
    
    print()
    print_header("🚀 PRÓXIMOS PASSOS")
    print("1. Execute os testes: python tests/run_tests.py")
    print("2. Inicie o servidor: python api_server.py")
    print("3. Acesse: http://localhost:5000")
    print("4. Teste a aba 'Conexões MCP'")
    print("5. Verifique os logs em: logs/api_server.log")
    print()
    
    return 0 if percentage == 100 else 1

if __name__ == '__main__':
    sys.exit(main())
