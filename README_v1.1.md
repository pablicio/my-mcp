# 🚀 MCP Personal Server v1.1.0

Servidor extensível baseado no Model Context Protocol (MCP) para gerenciamento pessoal de tarefas, notas e arquivos, com interface web moderna e monitoramento de conexões.

## ✨ Novidades v1.1.0

### 🔧 Correções Principais
- ✅ **Problema de criação de tarefas via Claude CORRIGIDO**
- ✅ Sistema de monitoramento de conexões MCP implementado
- ✅ Nova aba de visualização de clientes conectados
- ✅ Testes organizados e documentados em `tests/`

### 🆕 Novas Funcionalidades
- 📡 **Monitor de Conexões MCP** - Rastreie clientes conectados em tempo real
- 🤖 **Visualização de Clientes** - Veja Claude Desktop e outros clientes
- 📊 **Métricas de Uso** - Estatísticas de requisições e ferramentas usadas
- 🧪 **Suite de Testes Completa** - 14+ testes de conexão MCP

## 📋 Funcionalidades

### Core
- ✅ **Gerenciamento de Tarefas** - Crie, liste, complete e delete tarefas
- ✅ **Sistema de Notas** - Notas com tags e busca
- ✅ **Calendário** - Gerenciamento de eventos
- ✅ **Filesystem** - Acesso seguro a arquivos e diretórios
- 🆕 **Monitor de Conexões** - Rastreamento de clientes MCP

### Interface Web
- 🎨 Dashboard moderno e responsivo
- 📊 Estatísticas em tempo real
- 📋 Gerenciamento visual de tarefas
- 📝 Editor de notas
- 🆕 **Aba de Conexões MCP** - Visualize clientes conectados
- 📊 Visualizador de logs
- 🔄 Auto-refresh de dados

### Integração MCP
- 🔌 Compatível com Claude Desktop
- 🛠️ 7 ferramentas MCP disponíveis
- 📡 Monitoramento de uso em tempo real
- 🔍 Rastreamento de atividades

## 🚀 Início Rápido

### 1. Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd mcp-tools2

# Instale dependências
pip install -r requirements.txt

# Configure (se necessário)
python setup.py
```

### 2. Iniciar Servidor Web

```bash
# Inicie a API REST
python api_server.py

# Acesse em:
# http://localhost:5000
```

### 3. Configurar Claude Desktop

Adicione ao arquivo de configuração do Claude (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "personal-server": {
      "command": "python",
      "args": ["C:/projetos/IA/mcp/mcp-tools2/main.py"],
      "cwd": "C:/projetos/IA/mcp/mcp-tools2"
    }
  }
}
```

## 📊 Interface Web

### Dashboard
- Visão geral de tarefas, eventos e notas
- Estatísticas em tempo real
- Acesso rápido às funcionalidades principais

### Aba de Tarefas
- Criar novas tarefas com prioridade
- Filtrar por status (todas, pendentes, concluídas)
- Marcar como concluída ou deletar
- Busca em tempo real

### 🆕 Aba de Conexões MCP
**Nova funcionalidade!**
- 📡 Visualize clientes MCP conectados
- 🤖 Identifique Claude Desktop, Web Dashboard, etc.
- 📊 Métricas de requisições por cliente
- 🔧 Lista de ferramentas MCP utilizadas
- ⚡ Última atividade de cada cliente
- 🟢 Status de conexão em tempo real

### Aba de Notas
- Criar notas com tags
- Visualizar conteúdo completo
- Organização por data

### Aba de Logs
- Visualização de logs do sistema
- Filtros por tipo (info, warning, error)
- Busca em tempo real
- Auto-scroll

## 🛠️ Ferramentas MCP Disponíveis

### Tarefas
1. **create_task** - Criar nova tarefa
2. **list_tasks** - Listar tarefas
3. **complete_task** - Marcar como concluída
4. **delete_task** - Deletar tarefa
5. **search_tasks** - Buscar por texto

### Notas
6. **create_note** - Criar nova nota
7. **list_notes** - Listar notas

## 🧪 Testes

### Estrutura
```
tests/
├── unit/              # Testes unitários
├── integration/       # Testes de API
├── mcp/              # Testes MCP/Claude
│   └── test_claude_connection.py  # 14 testes
├── run_tests.py      # Menu interativo
└── *.bat            # Scripts Windows
```

### Executar Testes

```bash
# Menu interativo
python tests/run_tests.py

# Testes específicos
pytest tests/unit/ -v
pytest tests/integration/ -v  # Requer servidor rodando
pytest tests/mcp/ -v

# Todos os testes
pytest tests/ -v

# Via batch (Windows)
tests\run_all_tests.bat
```

### Testes MCP Implementados
- ✅ Inicialização do servidor
- ✅ Registro de ferramentas
- ✅ Criação de tarefas via MCP
- ✅ Listagem e busca
- ✅ Conclusão de tarefas
- ✅ Criação de notas
- ✅ Persistência de dados
- ✅ Tratamento de erros
- ✅ Operações concorrentes
- ✅ Conformidade com protocolo
- ✅ Workflows completos

## 📡 API REST

### Endpoints Principais

#### Status
```http
GET /api/status
```

#### Tarefas
```http
GET  /api/tasks
POST /api/tasks
POST /api/tasks/:id/complete
DELETE /api/tasks/:id
GET  /api/search/tasks?q=query
```

#### Notas
```http
GET  /api/notes
POST /api/notes
```

#### 🆕 Conexões MCP
```http
GET /api/connections
```
Retorna informações sobre clientes MCP conectados:
```json
{
  "clients": [
    {
      "client_id": "claude-desktop",
      "client_name": "Claude Desktop App",
      "status": "active",
      "connected_at": "2025-10-19T10:30:00",
      "last_activity": "2025-10-19T11:45:00",
      "requests_count": 42,
      "tools_used": ["create_task", "list_tasks", ...]
    }
  ],
  "stats": {
    "total_clients": 3,
    "active_clients": 2,
    "total_requests": 127
  }
}
```

#### Métricas
```http
GET /api/metrics
```
Agora inclui estatísticas de conexões MCP

#### Logs
```http
GET /api/logs?limit=100&level=all
```

## 🔧 Configuração

### Arquivo .env
```env
DEBUG=true
LOG_LEVEL=INFO
TASKS_DB_PATH=data/tasks.json
```

### Diretórios Permitidos
Configure em `config/settings.py`:
```python
ALLOWED_DIRECTORIES = [
    "C:/projetos",
    "C:/documentos"
]
```

## 📊 Monitoramento

### Logs
- **Servidor MCP**: `logs/mcp_server.log`
- **API REST**: `logs/api_server.log`
- **Conexões**: `data/mcp_connections.json`

### Métricas em Tempo Real
- Total de tarefas
- Taxa de conclusão
- Tarefas por prioridade
- 🆕 Clientes conectados
- 🆕 Requisições por cliente
- 🆕 Ferramentas mais usadas

## 🔍 Validação

Execute o script de validação para verificar se todas as correções foram aplicadas:

```bash
python validate_fixes.py
```

## 📚 Documentação Adicional

- [`CHANGELOG_FIXES.md`](CHANGELOG_FIXES.md) - Detalhes de todas as correções
- [`tests/README.md`](tests/README.md) - Guia completo de testes
- [`QUICKSTART_WEB.md`](QUICKSTART_WEB.md) - Guia rápido da interface web

## 🤝 Uso com Claude

### Criar Tarefa
```
Crie uma tarefa chamada "Estudar MCP" com prioridade alta
```

### Listar Tarefas
```
Liste todas as minhas tarefas pendentes
```

### Completar Tarefa
```
Marque a tarefa #5 como concluída
```

### Criar Nota
```
Crie uma nota sobre conexões MCP com tag "documentação"
```

### 🆕 Verificar Conexões
```
Mostre os clientes conectados ao servidor MCP
```

## 🛡️ Segurança

- ✅ Acesso restrito a diretórios configurados
- ✅ Validação de entrada em todas as ferramentas
- ✅ Logs detalhados de atividades
- ✅ Monitoramento de clientes conectados
- ✅ Sem armazenamento de credenciais

## 🐛 Troubleshooting

### Tarefas não sendo criadas via Claude
✅ **CORRIGIDO na v1.1.0!**
- Sistema de monitoramento implementado
- Verificar aba "Conexões MCP" no dashboard
- Logs em `logs/api_server.log`

### Servidor não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar configuração
python validate_fixes.py
```

### Interface web não carrega
```bash
# Verificar se servidor está rodando
python api_server.py

# Acessar: http://localhost:5000
```

### Testes falhando
```bash
# Verificar estrutura
python validate_fixes.py

# Executar testes específicos
pytest tests/mcp/ -v --tb=short
```

## 📈 Performance

- ⚡ Resposta < 100ms para operações CRUD
- 📊 Suporta 1000+ tarefas sem degradação
- 🔄 Auto-refresh a cada 5 segundos
- 💾 Persistência em JSON (rápida e confiável)

## 🗺️ Roadmap

### Próximas Versões
- [ ] Autenticação de clientes MCP
- [ ] Dashboard de métricas históricas
- [ ] Alertas de conexões perdidas
- [ ] Export de dados de conexões
- [ ] Gráficos de uso ao longo do tempo
- [ ] Suporte a múltiplos usuários
- [ ] Sincronização com Google Calendar
- [ ] Notificações push

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙏 Agradecimentos

- Anthropic pelo Claude e protocolo MCP
- Comunidade Python
- Todos os contribuidores

## 📞 Suporte

Para problemas ou dúvidas:
1. Consulte a documentação
2. Verifique issues existentes
3. Execute `python validate_fixes.py`
4. Verifique logs em `logs/`
5. Consulte a aba "Conexões MCP" no dashboard

---

**Versão**: 1.1.0  
**Data**: 19/10/2025  
**Status**: ✅ Estável e Testado  
**Última Atualização**: Sistema de monitoramento MCP implementado
