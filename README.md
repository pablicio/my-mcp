# 🎯 MCP SERVER PESSOAL v1.0.0

> Servidor MCP extensível para uso pessoal com Claude Desktop

## 🚀 Início Rápido (30 segundos)

```bash
# 1. Execute o menu interativo
run_tests.bat

# 2. Escolha [1] para testar
# 3. Escolha [2] para iniciar
# 4. Abra Claude Desktop e teste!
```

**🎉 Pronto!** Agora você pode usar comandos como:
- `"liste minhas tarefas"`
- `"crie uma nota sobre Python"`
- `"liste arquivos em C:\projetos"`

---

## 📚 Documentação

- **[QUICKSTART_VISUAL.md](QUICKSTART_VISUAL.md)** - Guia visual rápido ⭐
- **[GUIA_TESTES.md](GUIA_TESTES.md)** - Como testar e verificar conexão
- **[COMO_USAR.md](COMO_USAR.md)** - Documentação completa

---

## ✨ Funcionalidades

### 📋 Gerenciamento de Tarefas
- Criar, listar, completar e deletar tarefas
- Buscar tarefas por texto
- Filtrar por status (pendente/concluída)
- Definir prioridades e datas limite

### 📝 Sistema de Notas
- Criar notas com tags
- Listar notas recentes
- Organização simples e eficiente

### 📁 Acesso a Arquivos
- Ler e escrever arquivos
- Listar diretórios
- Buscar arquivos
- Controle de permissões

### 📅 Calendário Google (Opcional)
- Criar eventos
- Listar próximos eventos
- Integração OAuth2

---

## 🛠️ Ferramentas Disponíveis

### Menu Interativo (`run_tests.bat`)

```
╔══════════════════════════════════════════════════════════════════╗
║         MCP SERVER PESSOAL - MENU DE TESTE E EXECUÇÃO          ║
╚══════════════════════════════════════════════════════════════════╝

[1] 🧪 Testar Servidor      → Verifica funcionamento
[2] 🚀 Iniciar Servidor     → Modo com feedback visual
[3] 📊 Monitor Real-time    → Dashboard de atividade
[4] 📝 Ver Logs            → Logs em tempo real
[5] 🔍 Ver Status          → Status atual do servidor
[6] 🧹 Limpar Logs         → Remove arquivos de log
[7] ❌ Sair
```

### Scripts Individuais

| Script | Descrição |
|--------|-----------|
| `test_connection.py` | Executa bateria de testes completa |
| `main_verbose.py` | Servidor com feedback detalhado |
| `monitor.py` | Monitor visual em tempo real |
| `main.py` | Servidor normal (produção) |

---

## 📊 Como Verificar se Está Funcionando

### Método 1: Testes Automáticos (Recomendado)

```bash
run_tests.bat → [1] Testar Servidor
```

**Resultado esperado:**
```
✅ INITIALIZATION       PASSOU
✅ MODULES             PASSOU
✅ TASKS               PASSOU
✅ FILESYSTEM          PASSOU
✅ TOOLS               PASSOU

🎉 TODOS OS TESTES PASSARAM!
```

### Método 2: Monitor Visual

```bash
run_tests.bat → [3] Monitor em Tempo Real
```

Mostra:
- Status do servidor (rodando/parado)
- Estatísticas de logs
- Contador de tarefas
- Últimas linhas do log

### Método 3: Teste no Claude Desktop

1. Inicie o servidor: `run_tests.bat → [2]`
2. Abra Claude Desktop
3. Digite: `"liste minhas tarefas"`
4. Se funcionar, está conectado! ✅

---

## 🔧 Configuração

### Arquivo `.env`

```ini
# Debug
DEBUG=False

# Diretórios permitidos (separados por vírgula)
ALLOWED_DIRECTORIES="C:\projetos\IA,C:\Users\PC Gamer\Documents"

# Logs
LOG_LEVEL=INFO
LOG_FILE=./logs/mcp_server.log

# Tarefas
TASKS_DB_PATH=./data/tasks.json

# Google Calendar (opcional)
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_secret
```

### Configuração no Claude Desktop

Arquivo: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "personal-server": {
      "command": "C:\\projetos\\IA\\mcp\\mcp-tools2\\venv\\Scripts\\python.exe",
      "args": ["C:\\projetos\\IA\\mcp\\mcp-tools2\\main.py"]
    }
  }
}
```

---

## 🐛 Solução de Problemas

### ❌ Servidor não inicia

```bash
# 1. Verifique dependências
venv\Scripts\activate
pip install -r requirements.txt

# 2. Teste com modo verbose
python main_verbose.py

# 3. Veja os logs
type logs\mcp_server.log
```

### ❌ Claude não reconhece os comandos

1. **Reinicie Claude Desktop completamente**
2. **Verifique configuração:** `%APPDATA%\Claude\claude_desktop_config.json`
3. **Monitore logs:** `run_tests.bat → [4]`
4. **Execute testes:** `run_tests.bat → [1]`

### ❌ Testes falharam

```bash
# 1. Ative debug
echo DEBUG=True >> .env

# 2. Execute testes novamente
python test_connection.py

# 3. Veja erros detalhados nos logs
```

---

## 📦 Estrutura do Projeto

```
mcp-tools2/
├── 📄 README.md                    ⭐ Este arquivo
├── 📄 QUICKSTART_VISUAL.md         🚀 Guia visual rápido
├── 📄 GUIA_TESTES.md              🧪 Como testar
├── 📄 COMO_USAR.md                📚 Documentação completa
│
├── 🎮 run_tests.bat               ⭐ Menu principal
├── 🧪 test_connection.py          Testes automáticos
├── 📊 monitor.py                  Monitor visual
├── 🚀 main_verbose.py             Servidor com feedback
├── ⚙️  main.py                     Servidor normal
│
├── core/                          Núcleo do servidor
│   ├── server.py                 Servidor MCP principal
│   └── registry.py               Registro de ferramentas
│
├── modules/                       Módulos funcionais
│   ├── tasks/                    Gerenciamento de tarefas
│   ├── filesystem/               Acesso a arquivos
│   └── calendar/                 Integração com Google
│
├── config/                        Configurações
│   ├── settings.py              Configurações globais
│   └── logging.py               Sistema de logs
│
├── logs/                         Arquivos de log
│   └── mcp_server.log           Log principal
│
└── data/                         Dados persistentes
    └── tasks.json               Banco de tarefas
```

---

## 🎯 Casos de Uso

### Desenvolvimento

```bash
# Terminal 1: Servidor com feedback
run_tests.bat → [2]

# Terminal 2: Monitor de atividade
run_tests.bat → [3]

# Trabalhar normalmente no Claude Desktop
```

### Produção (dia a dia)

```bash
# Iniciar servidor
run_tests.bat → [2]

# Usar Claude Desktop normalmente
# O servidor roda em background
```

### Debugging

```bash
# 1. Ativar debug
echo DEBUG=True > .env

# 2. Ver logs ao vivo
run_tests.bat → [4]

# 3. Usar Claude Desktop e ver o que acontece
```

---

## 📝 Comandos Exemplo no Claude

```
# Tarefas
"crie uma tarefa: Estudar Python"
"liste minhas tarefas pendentes"
"complete a tarefa 1"
"busque tarefas sobre Python"
"delete a tarefa 2"

# Notas
"crie uma nota sobre MCP Server"
"liste minhas últimas notas"

# Arquivos
"liste os arquivos em C:\projetos\IA"
"leia o arquivo README.md"
"crie um arquivo teste.txt com 'Hello World'"
"busque arquivos .py no diretório"
```

---

## 🔄 Atualizações

### v1.0.0 (2025-10-18)
- ✅ Sistema de testes automáticos
- ✅ Menu interativo (run_tests.bat)
- ✅ Monitor visual em tempo real
- ✅ Modo verbose com feedback
- ✅ Documentação completa
- ✅ Melhor tratamento de erros
- ✅ Guias visuais (QUICKSTART_VISUAL.md, GUIA_TESTES.md)

---

## 🤝 Contribuindo

Este é um projeto pessoal, mas melhorias são bem-vindas!

1. Faça fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

MIT License - use como quiser!

---

## 🆘 Precisa de Ajuda?

1. **Leia primeiro:** [QUICKSTART_VISUAL.md](QUICKSTART_VISUAL.md) ⭐
2. **Testes:** [GUIA_TESTES.md](GUIA_TESTES.md)
3. **Documentação:** [COMO_USAR.md](COMO_USAR.md)
4. **Execute os testes:** `run_tests.bat → [1]`
5. **Veja os logs:** `run_tests.bat → [4]`

---

## 🎉 Pronto para Começar?

```bash
run_tests.bat
```

**É só isso!** O menu vai te guiar. 🚀

---

**Desenvolvido com ❤️ para integração com Claude Desktop**

*Última atualização: 18/10/2025*
