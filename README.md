# 🚀 MCP Server Pessoal v1.0.0

> Servidor extensível baseado no Model Context Protocol (MCP) para uso com Claude Desktop

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.2.0-green.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Índice

- [Características](#-características)
- [Instalação Rápida](#-instalação-rápida)
- [Configuração](#️-configuração)
- [Uso](#-uso)
- [Testes](#-testes)
- [Desenvolvimento](#️-desenvolvimento)
- [Troubleshooting](#-troubleshooting)
- [Documentação](#-documentação)

---

## ✨ Características

- 🔒 **Segurança**: Validação rigorosa de caminhos e controle de acesso por diretório
- 📁 **Sistema de Arquivos**: Leitura, escrita, busca e gerenciamento completo
- ✅ **Tarefas**: Sistema de gerenciamento de tarefas com prioridades e prazos
- 📅 **Google Calendar**: Integração opcional com sua agenda Google
- 🛠️ **Extensível**: Arquitetura modular para adicionar novos recursos facilmente
- 📊 **Logging**: Sistema completo de logs para debugging e auditoria

---

## 🚀 Instalação Rápida

### Pré-requisitos

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Claude Desktop** instalado
- Windows, macOS ou Linux

### Setup Automatizado (3 minutos)

```bash
# 1. Navegue até o diretório do projeto
cd C:\projetos\IA\mcp\mcp-tools2

# 2. Execute o setup
python setup.py

# 3. Siga as instruções na tela
```

O script irá automaticamente:
- ✅ Verificar Python 3.9+
- ✅ Instalar todas as dependências
- ✅ Criar arquivo .env com configurações
- ✅ Configurar Claude Desktop
- ✅ Criar estrutura de diretórios
- ✅ Executar testes de validação

**📚 Guia Detalhado:** Veja [QUICKSTART.md](QUICKSTART.md) para instruções passo a passo.

---

## ⚙️ Configuração

### 1. Arquivo .env

Edite o arquivo `.env` (criado pelo setup ou copie de `.env.example`):

```env
# Diretórios permitidos (USE CAMINHOS ABSOLUTOS!)
# Windows
ALLOWED_DIRECTORIES=C:\\Users\\SeuUsuario\\Documents,C:\\Users\\SeuUsuario\\Desktop

# Linux/Mac
ALLOWED_DIRECTORIES=/home/usuario/Documents,/home/usuario/Desktop

# Configurações do servidor
DEBUG=false
LOG_LEVEL=INFO

# Google Calendar (opcional)
# GOOGLE_CLIENT_ID=seu_client_id
# GOOGLE_CLIENT_SECRET=seu_client_secret
```

**⚠️ IMPORTANTE:** Use sempre caminhos absolutos!

### 2. Claude Desktop

O setup configura automaticamente, mas se necessário, edite manualmente:

**Localização:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Conteúdo:**
```json
{
  "mcpServers": {
    "personal-server": {
      "command": "python",
      "args": ["C:\\caminho\\completo\\para\\main.py"],
      "env": {
        "PYTHONPATH": "C:\\caminho\\completo\\para\\projeto"
      }
    }
  }
}
```

---

## 🎮 Uso

### Iniciar o Servidor

```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Ou diretamente
python main.py
```

### Usar no Claude Desktop

1. **Reinicie o Claude Desktop** (feche completamente!)
2. Abra uma nova conversa
3. Digite comandos naturais

**Exemplos de Comandos:**

```
📁 Arquivos:
• Liste os arquivos na minha pasta Documents
• Leia o arquivo README.md
• Crie arquivo teste.py com código Hello World
• Procure arquivos .txt em Documents recursivamente

✅ Tarefas:
• Crie tarefa: "Revisar documentação" com prioridade alta
• Mostre minhas tarefas pendentes
• Marque tarefa #3 como concluída

📅 Calendar (se configurado):
• Crie evento "Reunião de equipe" amanhã às 14h
• Quais são meus compromissos hoje?
```

---

## 🧪 Testes

### Teste Rápido
```bash
python -m tests.quick_test
```

### Testes Unitários
```bash
pytest tests/unit/ -v
```

### Testes de Integração
```bash
pytest tests/integration/ -v
```

### Todos os Testes com Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

**📚 Mais sobre testes:** Veja estrutura completa em `tests/`

---

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
mcp-tools2/
├── main.py              # Ponto de entrada
├── setup.py             # Script de instalação
├── dev.py               # Ferramentas de desenvolvimento
│
├── config/              # Configurações centralizadas
│   ├── settings.py      # Settings com Pydantic
│   └── logging.py       # Configuração de logs
│
├── core/                # Núcleo do servidor MCP
│   ├── server.py        # Servidor principal
│   ├── registry.py      # Registro de ferramentas
│   └── security.py      # Validações de segurança
│
├── modules/             # Módulos funcionais (plugins)
│   ├── base.py          # Classe base
│   ├── filesystem/      # Sistema de arquivos
│   ├── tasks/           # Gerenciamento de tarefas
│   └── calendar/        # Google Calendar
│
├── utils/               # Utilitários compartilhados
│
└── tests/               # Testes centralizados
    ├── quick_test.py    # Teste rápido
    ├── unit/            # Testes unitários
    └── integration/     # Testes de integração
```

### Ferramentas de Desenvolvimento

```bash
# Menu interativo
python dev.py

# Opções disponíveis:
# 1. Testes rápidos
# 2. Testes unitários
# 3. Testes de integração
# 4. Coverage
# 5. Limpar projeto
# 6. Instalar dependências
# 7. Iniciar em modo debug
# 8. Verificar código
# 9. Verificar configuração
```

### Adicionar Novo Módulo

1. Crie diretório em `modules/`
2. Implemente classe herdando `BaseModule`
3. Registre em `core/server.py`

**📚 Guia Completo:** Veja [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🐛 Troubleshooting

### Claude não encontra o servidor

1. Reinicie o Claude Desktop **completamente**
2. Verifique `claude_desktop_config.json`
3. Teste manualmente: `python main.py`
4. Consulte logs: `logs/mcp_server.log`

### Erro "Diretório não permitido"

1. Verifique `ALLOWED_DIRECTORIES` no `.env`
2. Use caminhos absolutos
3. Certifique-se que os diretórios existem

### Erro de importação

```bash
pip install -r requirements.txt --force-reinstall
```

### Logs detalhados

```bash
# Ative no .env
DEBUG=true
LOG_LEVEL=DEBUG

# Ver logs em tempo real
# Windows PowerShell:
Get-Content logs\mcp_server.log -Wait

# Linux/Mac:
tail -f logs/mcp_server.log
```

---

## 📚 Documentação

### Documentos Principais

| Documento | Descrição |
|-----------|-----------|
| **[README.md](README.md)** | Este arquivo - Visão geral completa |
| **[QUICKSTART.md](QUICKSTART.md)** | Guia de início rápido (3 minutos) |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Guia de desenvolvimento |
| **[CHANGELOG.md](CHANGELOG.md)** | Histórico de mudanças |
| **[REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)** | Resumo da refatoração |

### Scripts Úteis

| Script | Descrição |
|--------|-----------|
| `python dev.py` | Menu interativo de desenvolvimento |
| `python -m tests.quick_test` | Teste rápido de validação |
| `python clean_project.py` | Remove arquivos desnecessários |
| `python show_improvements.py` | Mostra melhorias implementadas |
| `COMANDOS_PRONTOS.bat` | Menu Windows interativo |

---

## 🔒 Segurança

O servidor implementa múltiplas camadas de segurança:

- ✅ **Validação de Caminhos**: Proteção contra path traversal
- ✅ **Allowlist**: Apenas diretórios configurados são acessíveis
- ✅ **Sanitização**: Nomes de arquivos são sanitizados
- ✅ **Limites**: Tamanho máximo de arquivo (10MB configurável)
- ✅ **Timeout**: Operações têm timeout (30s configurável)
- ✅ **Logging**: Todas as operações são registradas

**💡 Dica:** Configure apenas os diretórios necessários em `ALLOWED_DIRECTORIES`.

---

## 📊 Comandos Úteis

```bash
# Iniciar servidor
python main.py
start.bat              # Windows
./start.sh             # Linux/Mac

# Testes
python -m tests.quick_test          # Rápido
pytest tests/ -v                    # Completo
pytest tests/ --cov=.               # Com coverage

# Desenvolvimento
python dev.py                       # Menu interativo
python clean_project.py             # Limpar arquivos antigos

# Windows
COMANDOS_PRONTOS.bat                # Menu Windows
```

---

## 🆘 Suporte

- 📖 **Documentação:** Veja arquivos `.md` na raiz
- 📊 **Logs:** `./logs/mcp_server.log`
- 🐛 **Debug:** `DEBUG=true python main.py`
- 📝 **Checklist:** [POST_REFACTOR_CHECKLIST.md](POST_REFACTOR_CHECKLIST.md)

---

## 📝 Licença

MIT License - Use como desejar!

---

## 🎉 Agradecimentos

Desenvolvido com ❤️ usando:
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Claude](https://claude.ai) by Anthropic
- [Pydantic](https://docs.pydantic.dev)
- [FastMCP](https://github.com/jlowin/fastmcp)

---

<div align="center">

**[🏠 Início](#-mcp-server-pessoal-v100)** • **[⚡ Quick Start](QUICKSTART.md)** • **[📖 Contribuir](CONTRIBUTING.md)** • **[📝 Changelog](CHANGELOG.md)**

</div>
