# 🎯 Guia de Início Rápido

## Para Começar AGORA (3 minutos)

### 1. Instalação Automática
```bash
python setup.py
```

O script irá:
- ✅ Verificar Python 3.9+
- ✅ Instalar todas as dependências
- ✅ Criar arquivo .env
- ✅ Configurar Claude Desktop
- ✅ Executar testes

### 2. Testar
```bash
python -m tests.quick_test
```

### 3. Iniciar
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

### 4. Reiniciar Claude Desktop

Feche completamente e abra novamente.

### 5. Testar no Claude

```
Liste os arquivos na minha pasta Documents
```

## ⚡ Atalhos Úteis

### Windows
```batch
COMANDOS_PRONTOS.bat    # Menu interativo
start.bat               # Iniciar servidor
python dev.py           # Ferramentas dev
```

### Linux/Mac
```bash
./start.sh              # Iniciar servidor
python3 dev.py          # Ferramentas dev
```

## 🆘 Problemas Comuns

### Claude não encontra o servidor
1. Reinicie Claude Desktop (feche tudo)
2. Verifique: `python main.py` funciona?
3. Veja logs: `logs/mcp_server.log`

### Erro de importação
```bash
pip install -r requirements.txt --force-reinstall
```

### Diretório não permitido
1. Edite `.env`
2. Configure `ALLOWED_DIRECTORIES` com caminhos absolutos
3. Reinicie servidor

## 📚 Documentação Completa

- **README.md** - Documentação principal
- **CONTRIBUTING.md** - Guia de desenvolvimento
- **CHANGELOG.md** - Histórico de mudanças

## 🎉 Pronto!

Seu servidor MCP está pronto para uso. Divirta-se! 🚀
