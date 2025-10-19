#!/bin/bash
# 🚀 Script para iniciar o MCP Server no Linux/Mac

echo "============================================================"
echo "  MCP Server Pessoal v1.0.0"
echo "============================================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRO: Python não encontrado!"
    echo "💡 Instale Python 3.9+ antes de continuar"
    exit 1
fi

# Verificar versão do Python
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.9"

if (( $(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc -l) )); then
    echo "❌ ERRO: Python $PYTHON_VERSION encontrado"
    echo "💡 Necessário Python 3.9 ou superior"
    exit 1
fi

# Verificar diretório
if [ ! -f "main.py" ]; then
    echo "❌ ERRO: main.py não encontrado!"
    echo "💡 Execute no diretório do projeto"
    exit 1
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo "⚠️  AVISO: Arquivo .env não encontrado"
    echo "💡 Execute primeiro: python3 setup.py"
    echo ""
    read -p "Continuar mesmo assim? (s/N): " continue
    if [ "$continue" != "s" ] && [ "$continue" != "S" ]; then
        exit 1
    fi
fi

echo "✅ Iniciando servidor MCP..."
echo ""
echo "🔧 Para parar: Ctrl+C"
echo "📊 Logs: logs/mcp_server.log"
echo "💡 Depois de iniciar, reinicie o Claude Desktop"
echo ""
echo "============================================================"
echo ""

# Iniciar o servidor
python3 main.py

# Verificar código de saída
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Servidor encerrou com erro"
    echo "💡 Verifique os logs em: logs/mcp_server.log"
    exit 1
fi
