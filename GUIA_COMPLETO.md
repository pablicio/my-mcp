# 📘 Guia Completo - MCP Server Pessoal v1.0.0

## 🎯 Visão Geral

Este é um servidor MCP (Model Context Protocol) completo e funcional que permite ao Claude Desktop acessar seus recursos locais de forma segura e controlada.

### ✨ Características Principais

- **🔒 Segurança Robusta**: Validação rigorosa de caminhos, controle de acesso por diretório
- **📁 Gerenciamento de Arquivos**: Leitura, escrita, busca e organização
- **✅ Sistema de Tarefas**: Gerenciamento de tarefas com prioridades
- **📅 Google Calendar**: Integração com sua agenda (opcional)
- **🛠️ Extensível**: Arquitetura modular para adicionar novas funcionalidades
- **📊 Logging Completo**: Rastreamento de todas as operações

---

## 📦 Instalação

### Método 1: Setup Automatizado (Recomendado)

```bash
# 1. Clone ou baixe o projeto
cd C:\projetos\IA\mcp\mcp-tools2

# 2. Execute o setup
python setup.py

# 3. Siga as instruções na tela
```

O script irá:
- ✅ Verificar Python 3.9+
- ✅ Instalar dependências
- ✅ Criar arquivo .env
- ✅ Configurar Claude Desktop
- ✅ Criar estrutura de diretórios
- ✅ Testar instalação

### Método 2: Manual

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar ambiente
cp .env.example .env
# Edite .env com seus caminhos

# 3. Criar diretórios
mkdir logs data

# 4. Configurar Claude Desktop (veja seção abaixo)
```

---

## ⚙️ Configuração

### 1. Arquivo .env

Edite `.env` com suas configurações:

```env
# Diretórios permitidos (use caminhos ABSOLUTOS)
# Windows
ALLOWED_DIRECTORIES=C:\Users\SeuUsuario\Documents,C:\Users\SeuUsuario\Desktop,C:\projetos

# Linux/Mac
ALLOWED_DIRECTORIES=/home/usuario/Documents,/home/usuario/Desktop,/home/usuario/projetos

# Servidor
DEBUG=false
LOG_LEVEL=INFO

# Google Calendar (Opcional)
# GOOGLE_CLIENT_ID=seu_client_id
# GOOGLE_CLIENT_SECRET=seu_client_secret
```

**⚠️ IMPORTANTE**: Use sempre caminhos absolutos!

### 2. Claude Desktop

**Localização do arquivo de configuração:**

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Conteúdo do arquivo:**

```json
{
  "mcpServers": {
    "personal-server": {
      "command": "python",
      "args": ["C:\\projetos\\IA\\mcp\\mcp-tools2\\main.py"],
      "env": {
        "PYTHONPATH": "C:\\projetos\\IA\\mcp\\mcp-tools2"
      }
    }
  }
}
```

**Dicas:**
- Use caminhos absolutos
- No Windows, use `\\` ou `/` (nunca `\` sozinho)
- Teste o caminho no terminal antes

---

## 🚀 Execução

### Iniciar o Servidor

```bash
# Modo normal
python main.py

# Modo debug (mais logs)
DEBUG=true python main.py
```

**Saída esperada:**
```
============================================================
🚀 MCP SERVER PESSOAL v1.0.0
============================================================
🌐 Host: localhost:8080
🐛 Debug: Disabled
✅ Servidor MCP inicializado com sucesso!
🔧 Para parar: Ctrl+C
📊 Logs: ./logs/mcp_server.log
```

### Usar no Claude Desktop

1. **Reinicie o Claude Desktop** (importante!)
2. Abra uma nova conversa
3. Digite um comando, por exemplo:
   ```
   Liste os arquivos na minha pasta Documents
   ```

---

## 💡 Exemplos de Uso

### 📁 Gerenciamento de Arquivos

#### Listar Diretórios
```
Claude, liste os arquivos na minha pasta Documents
Mostre todos os arquivos Python na pasta projetos
```

#### Ler Arquivos
```
Leia o arquivo README.md do meu projeto
Mostre o conteúdo de config.json
```

#### Criar Arquivos
```
Crie um arquivo teste.py com um script Hello World
Salve este código em utils.py: [seu código]
```

#### Buscar Arquivos
```
Procure arquivos .txt na pasta Documents
Encontre todos os arquivos que contêm 'config' no nome
```

### ✅ Sistema de Tarefas

```
Crie uma tarefa: "Revisar documentação" com prioridade alta
Mostre minhas tarefas pendentes
Marque a tarefa #3 como concluída
```

### 📅 Google Calendar (se configurado)

```
Crie um evento "Reunião de equipe" amanhã às 14h
Quais são meus compromissos hoje?
Encontre eventos com "médico"
```

---

## 🔍 Verificação e Testes

### Teste Manual Rápido

```bash
# 1. Iniciar servidor
python main.py

# 2. No Claude Desktop, testar comando
"Liste arquivos no meu Documents"
```

### Verificar Configuração

```python
# Verificar settings
python -c "from config.settings import settings; print(settings.dict())"
```

---

## 🐛 Troubleshooting

### "Erro de importação"
```bash
pip install -r requirements.txt --force-reinstall
python --version  # Deve ser 3.9+
```

### "Diretório não permitido"
1. Verifique `ALLOWED_DIRECTORIES` em `.env`
2. Use caminhos absolutos
3. Teste: `python -c "from pathlib import Path; print(Path('seu_caminho').resolve())"`

### "Claude não encontra o servidor"
1. Reinicie o Claude Desktop completamente
2. Verifique `claude_desktop_config.json`
3. Teste: `python main.py`
4. Verifique logs: `logs/mcp_server.log`

### Logs Detalhados
```bash
# Ativar debug
echo "LOG_LEVEL=DEBUG" >> .env

# Ver logs em tempo real (Linux/Mac)
tail -f logs/mcp_server.log

# Windows PowerShell
Get-Content logs/mcp_server.log -Wait
```

---

## 📊 Estrutura do Projeto

```
mcp-tools2/
├── main.py              # Entrada do servidor
├── setup.py             # Setup automatizado
├── requirements.txt     # Dependências
├── .env                 # Configurações
├── README.md           # Documentação
├── GUIA_COMPLETO.md    # Este guia
│
├── config/             # Configurações
├── core/               # Núcleo do servidor
├── modules/            # Módulos funcionais
├── utils/              # Utilitários
├── tests/              # Testes
├── data/               # Dados
└── logs/               # Logs
```

---

## 🆘 Suporte

- 📖 Documentação: README.md
- 📊 Logs: `./logs/mcp_server.log`
- 🐛 Debug: `DEBUG=true python main.py`

---

**Desenvolvido com ❤️ usando Model Context Protocol**
