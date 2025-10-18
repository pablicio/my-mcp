#!/bin/bash
# Script para iniciar o MCP Server no Linux/Mac

echo "========================================"
echo "  MCP Server Pessoal - Inicialização"
echo "========================================"
echo ""

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRO: Python não encontrado!"
    echo "Instale Python 3.9+ antes de continuar"
    exit 1
fi

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ ERRO: main.py não encontrado!"
    echo "Execute este script no diretório do projeto"
    exit 1
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  AVISO: Arquivo .env não encontrado"
    echo "Execute: python3 setup.py"
    echo ""
    read -p "Continuar mesmo assim? (s/N): " continue
    if [ "$continue" != "s" ] && [ "$continue" != "S" ]; then
        exit 1
    fi
fi

echo "🚀 Iniciando servidor MCP..."
echo ""
echo "Para parar: Ctrl+C"
echo "Logs: logs/mcp_server.log"
echo ""

# Iniciar o servidor
python3 main.py
