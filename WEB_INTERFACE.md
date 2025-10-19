# 🌐 Interface Web do MCP Server

> Dashboard web moderno e funcional com integração completa ao backend

## 🚀 Início Rápido

```bash
# 1. Execute o servidor web
start_web_interface.bat

# 2. Abra no navegador
http://localhost:5000
```

**Pronto!** Agora você tem uma interface visual completa para gerenciar suas tarefas.

---

## ✨ Funcionalidades

### 📊 Dashboard em Tempo Real
- Status do servidor (online/offline)
- Contador de tarefas ativas
- Contador de notas
- Total de ferramentas disponíveis
- **Atualização automática a cada 5 segundos**

### 📋 Gerenciamento de Tarefas
- ✅ Criar novas tarefas
- ✅ Listar tarefas (pendentes/concluídas)
- ✅ Marcar como concluída
- ✅ Deletar tarefas
- ✅ Visualizar prioridades (alta/média/baixa)
- ✅ Ver datas limite
- ✅ Ver datas de criação

### 📝 Sistema de Notas
- Visualização de notas recentes
- Tags organizacionais
- Timestamps de criação

### 📊 Logs em Tempo Real
- Últimos 50 logs do servidor
- Código de cores por tipo (INFO, WARNING, ERROR, SUCCESS)
- Scroll automático para logs mais recentes
- Atualização automática

---

## 🎯 Como Usar

### 1. Instalar Dependências

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Instalar Flask
pip install flask flask-cors
```

### 2. Iniciar Servidor

```bash
# Opção 1: Usar o batch (recomendado)
start_web_interface.bat

# Opção 2: Manualmente
python api_server.py
```

### 3. Acessar Interface

Abra no navegador: **http://localhost:5000**

---

## 🔌 Endpoints da API

### Status
```
GET /api/status
```
Retorna status do servidor, estatísticas e últimos logs

**Resposta:**
```json
{
  "status": "running",
  "initialized": true,
  "modules": {
    "tasks": true,
    "filesystem": true,
    "calendar": false
  },
  "stats": {
    "tasks": 5,
    "notes": 2,
    "tools": 14
  },
  "timestamp": "2025-10-19T09:00:00"
}
```

### Tarefas

#### Listar Tarefas
```
GET /api/tasks?status=all&limit=50
```
**Parâmetros:**
- `status`: all | pending | completed
- `limit`: número máximo de tarefas

**Resposta:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Estudar Python",
      "description": "Aprender conceitos avançados",
      "priority": "high",
      "due_date": "2025-10-20",
      "completed": false,
      "created_at": "2025-10-19T09:00:00"
    }
  ],
  "total": 10,
  "filtered": 5
}
```

#### Criar Tarefa
```
POST /api/tasks
Content-Type: application/json

{
  "title": "Minha tarefa",
  "description": "Descrição detalhada",
  "priority": "medium",
  "due_date": "2025-10-25"
}
```

#### Completar Tarefa
```
POST /api/tasks/1/complete
```

#### Deletar Tarefa
```
DELETE /api/tasks/1
```

### Notas

#### Listar Notas
```
GET /api/notes?limit=20
```

#### Criar Nota
```
POST /api/notes
Content-Type: application/json

{
  "title": "Minha nota",
  "content": "Conteúdo da nota",
  "tags": "python,mcp,servidor"
}
```

### Logs

#### Obter Logs
```
GET /api/logs?limit=100
```

### Busca

#### Buscar Tarefas
```
GET /api/search/tasks?q=python
```

---

## 🎨 Design

### Tema Dark Moderno
- Cores vibrantes e contrastantes
- Animações suaves
- Feedback visual para ações
- Responsivo (funciona em mobile)

### Componentes
- **Cards de estatísticas** - Visão geral rápida
- **Abas de navegação** - Organização clara
- **Lista de tarefas** - Visualização detalhada
- **Formulários** - Criação intuitiva
- **Logs coloridos** - Debug facilitado
- **Toasts** - Notificações de ações

---

## 🔄 Atualização Automática

A interface atualiza automaticamente a cada 5 segundos:
- Status do servidor
- Estatísticas (tarefas, notas)
- Conteúdo da aba ativa (tarefas, notas ou logs)

**Desabilitar:** Comente a linha no final do `index.html`:
```javascript
// autoRefreshInterval = setInterval(() => { ... }, 5000);
```

---

## 🛠️ Estrutura Técnica

### Backend (api_server.py)
```
Flask REST API
├── Endpoints JSON
├── CORS habilitado
├── Integração com módulos MCP
└── Tratamento de erros
```

### Frontend (index.html)
```
Single Page Application
├── HTML5 + CSS3 + Vanilla JS
├── Fetch API para requisições
├── Animações CSS
├── Responsive design
└── Auto-refresh
```

### Dados (data/tasks.json)
```json
{
  "tasks": [...],
  "notes": [...],
  "last_updated": "..."
}
```

---

## 📊 Fluxo de Dados

```
┌─────────────────┐
│   Navegador     │
│  (index.html)   │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────┐
│   API Server    │
│ (api_server.py) │
└────────┬────────┘
         │ Python
         ↓
┌─────────────────┐
│  Tasks Module   │
│   (tools.py)    │
└────────┬────────┘
         │ JSON
         ↓
┌─────────────────┐
│  data/tasks.json│
└─────────────────┘
```

---

## 🐛 Solução de Problemas

### ❌ Erro "Servidor não conecta"

**Problema:** Interface mostra "Offline" ou "Erro de Conexão"

**Solução:**
```bash
# 1. Verificar se API está rodando
# Deve mostrar "Running on http://0.0.0.0:5000"

# 2. Testar endpoint manualmente
curl http://localhost:5000/api/status

# 3. Verificar firewall/antivírus
# Liberar porta 5000

# 4. Verificar logs
type logs\mcp_server.log
```

### ❌ Erro "Flask não instalado"

**Solução:**
```bash
pip install flask flask-cors
```

### ❌ Tarefas não aparecem

**Problema:** Lista vazia ou carregando infinitamente

**Solução:**
```bash
# 1. Verificar se módulo inicializou
# Logs devem mostrar: "Tasks inicializado com X tarefas"

# 2. Verificar arquivo de dados
type data\tasks.json

# 3. Criar tarefa manualmente via API
curl -X POST http://localhost:5000/api/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Teste\",\"description\":\"Tarefa de teste\"}"
```

### ❌ CORS Error

**Problema:** Erro de CORS no console do navegador

**Solução:**
```python
# Já está configurado no api_server.py
from flask_cors import CORS
CORS(app)

# Se persistir, acesse via http://localhost:5000
# (não via file:// ou outro domínio)
```

---

## 🎯 Próximos Passos

### Funcionalidades Planejadas
- [ ] Edição de tarefas existentes
- [ ] Filtros avançados (por data, prioridade)
- [ ] Busca de tarefas na interface
- [ ] Criação de notas na interface
- [ ] Exportar tarefas (CSV, JSON)
- [ ] Importar tarefas
- [ ] Estatísticas e gráficos
- [ ] Notificações de prazo
- [ ] Modo escuro/claro toggle
- [ ] Autenticação básica

### Melhorias Técnicas
- [ ] WebSockets para updates em tempo real
- [ ] Service Worker para offline
- [ ] Progressive Web App (PWA)
- [ ] Testes automatizados
- [ ] Docker container

---

## 💡 Dicas de Uso

### Desenvolvimento
```bash
# Terminal 1: API Server
python api_server.py

# Terminal 2: MCP Server (se quiser usar com Claude)
python main.py

# Navegador: Interface Web
http://localhost:5000
```

### Produção (uso diário)
```bash
# Apenas a interface web é suficiente
start_web_interface.bat

# Abrir navegador
http://localhost:5000
```

### Integração com Claude
```bash
# Terminal 1: API Server (interface web)
python api_server.py

# Terminal 2: MCP Server (Claude Desktop)
python main.py

# Agora você tem:
# - Interface web: http://localhost:5000
# - Claude Desktop: integração MCP
# - Dados sincronizados entre ambos
```

---

## 📝 Exemplos de Uso

### Criar Tarefa via Interface
1. Clique na aba "➕ Nova Tarefa"
2. Preencha título (obrigatório)
3. Adicione descrição (opcional)
4. Selecione prioridade
5. Defina data limite (opcional)
6. Clique "Criar Tarefa"
7. ✅ Tarefa criada e lista atualizada automaticamente

### Criar Tarefa via API
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar MCP",
    "description": "Aprender sobre Model Context Protocol",
    "priority": "high",
    "due_date": "2025-10-25"
  }'
```

### Criar Tarefa via Claude Desktop
```
"crie uma tarefa: Revisar código Python"
```

**Resultado:** A tarefa aparece em todos os três lugares:
- Interface web
- Resposta do Claude
- Arquivo `data/tasks.json`

---

## 🤝 Contribuindo

Quer melhorar a interface? Aqui estão algumas áreas:

### CSS/Design
- Adicionar mais animações
- Melhorar responsividade mobile
- Criar temas customizáveis
- Adicionar dark/light mode toggle

### JavaScript
- Implementar busca em tempo real
- Adicionar filtros dinâmicos
- Criar gráficos com Chart.js
- Adicionar drag & drop para prioridades

### Python/API
- Adicionar mais endpoints
- Implementar autenticação
- Criar sistema de backup
- Adicionar rate limiting

---

## 📚 Recursos

### Documentação Relacionada
- [README.md](README.md) - Documentação principal do MCP Server
- [QUICKSTART_VISUAL.md](QUICKSTART_VISUAL.md) - Guia visual rápido
- [GUIA_TESTES.md](GUIA_TESTES.md) - Como testar o servidor

### Tecnologias Utilizadas
- **Flask** - Framework web Python
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Vanilla JavaScript** - Frontend sem frameworks
- **CSS3** - Estilização moderna
- **HTML5** - Estrutura semântica

---

## 🎉 Conclusão

Agora você tem uma interface web completa e funcional para o MCP Server!

**Features principais:**
✅ Dashboard em tempo real
✅ Gerenciamento completo de tarefas
✅ Logs ao vivo
✅ Atualização automática
✅ Design moderno e responsivo
✅ API REST completa

**Próximos passos:**
1. Execute `start_web_interface.bat`
2. Abra http://localhost:5000
3. Comece a gerenciar suas tarefas! 🚀

---

**Desenvolvido com ❤️ para o MCP Server**

*Última atualização: 19/10/2025*
