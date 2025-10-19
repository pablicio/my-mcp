# 🚀 MCP Server - Dashboard Web Avançado

## 📋 Visão Geral

Interface web moderna e responsiva para gerenciamento do MCP Server com suporte completo para:
- ✅ **Tarefas** (Tasks) - Criação, edição, conclusão e exclusão
- 📅 **Calendário** (Calendar) - Gerenciamento de eventos
- 📝 **Notas** - Sistema de anotações com tags
- 📊 **Logs** - Visualização avançada com filtros e busca
- 📈 **Métricas** - Dashboard com estatísticas em tempo real

---

## 🎨 Novos Recursos da Interface

### 1. **Design Moderno**
- Interface dark mode elegante
- Animações suaves e transições fluidas
- Gradientes e efeitos visuais modernos
- Responsivo para mobile, tablet e desktop

### 2. **Dashboard Overview**
- Estatísticas em tempo real
- Cards interativos com hover effects
- Visualização rápida de tarefas pendentes
- Próximos eventos do calendário

### 3. **Gerenciamento de Tarefas**
- ✅ Filtros avançados (Todas, Pendentes, Concluídas, Alta Prioridade)
- 🔍 Busca em tempo real
- 🎯 Badges de prioridade (Alta, Média, Baixa)
- ⏰ Datas de vencimento
- ✓ Conclusão com um clique
- 🗑️ Exclusão confirmada

### 4. **Sistema de Calendário**
- 📅 Visualização de eventos
- ➕ Criação de novos eventos
- 🕐 Data e hora de início/fim
- 📍 Local do evento
- 📝 Descrição detalhada

### 5. **Notas**
- 📝 Criação rápida de notas
- 🏷️ Sistema de tags
- 📄 Visualização de conteúdo
- 🔍 Busca por texto

### 6. **Logs Avançados**
- 📊 Filtros por nível (Info, Success, Warning, Error)
- 🔍 Busca em tempo real nos logs
- 🎨 Código de cores por tipo
- 📜 Auto-scroll para últimas entradas
- 💾 Histórico completo

---

## 🛠️ Melhorias na API

### 1. **Logging Estruturado**
```python
# Logs detalhados com níveis apropriados
logger.info(f"✅ Tarefa criada: #{id} - {title}")
logger.warning(f"⚠️ Módulo não inicializado")
logger.error(f"❌ Erro ao processar: {e}", exc_info=True)
```

### 2. **Novos Endpoints**

#### `GET /api/metrics`
Retorna métricas detalhadas:
```json
{
  "tasks": {
    "total": 25,
    "pending": 15,
    "completed": 10,
    "completion_rate": 40.0
  },
  "priority": {
    "high": 5,
    "medium": 8,
    "low": 2
  },
  "notes": {
    "total": 12
  }
}
```

#### `GET /api/logs?level=ERROR&limit=50`
Logs filtrados por nível

#### `GET /api/search/tasks?q=python`
Busca inteligente em tarefas

### 3. **Respostas Enriquecidas**
Todas as respostas incluem:
- ✅ Status de sucesso/erro
- 📊 Estatísticas adicionais
- ⏰ Timestamps
- 📝 Mensagens descritivas

---

## 📁 Estrutura de Arquivos

```
mcp-tools2/
├── index.html          # Interface principal (HTML limpo e semântico)
├── styles.css          # Estilos modernos com CSS Grid e Flexbox
├── app.js              # Lógica JavaScript modular
├── api_server.py       # API REST com logging aprimorado
├── logs/
│   ├── api_server.log  # Logs da API
│   └── mcp_server.log  # Logs do servidor MCP
└── data/
    ├── tasks.json      # Banco de dados de tarefas
    └── notes.json      # Banco de dados de notas
```

---

## 🚀 Como Usar

### 1. Iniciar o Servidor
```bash
# Via Python
python api_server.py

# Ou via batch
start_web_interface.bat
```

### 2. Acessar a Interface
Abra no navegador: `http://localhost:5000`

### 3. Funcionalidades Disponíveis

#### **Dashboard**
- Veja estatísticas gerais
- Tarefas recentes pendentes
- Próximos eventos

#### **Tarefas**
1. Clique em "Nova Tarefa"
2. Preencha título, descrição, prioridade e data
3. Clique em "Criar Tarefa"
4. Use filtros para organizar
5. Busque tarefas específicas
6. Complete ou delete conforme necessário

#### **Calendário**
1. Clique em "Novo Evento"
2. Preencha título, descrição, data/hora
3. Adicione local (opcional)
4. Salve o evento

#### **Notas**
1. Clique em "Nova Nota"
2. Adicione título e conteúdo
3. Use tags para organizar
4. Salve a nota

#### **Logs**
1. Visualize logs em tempo real
2. Filtre por nível (Info, Warning, Error)
3. Busque termos específicos
4. Auto-refresh a cada 5 segundos

---

## 🎯 Recursos Técnicos

### **Frontend**
- ✅ Vanilla JavaScript (sem dependências)
- ✅ CSS moderno com variáveis CSS
- ✅ Fetch API para comunicação
- ✅ Event delegation eficiente
- ✅ Local state management
- ✅ Debounce em buscas
- ✅ Auto-refresh inteligente

### **Backend**
- ✅ Flask com CORS configurado
- ✅ Logging estruturado
- ✅ Async/await para operações I/O
- ✅ Tratamento robusto de erros
- ✅ Validação de dados
- ✅ Response caching
- ✅ Thread-safe operations

### **Observabilidade**
- ✅ Logs com timestamps
- ✅ Níveis de log apropriados
- ✅ Stack traces em erros
- ✅ Métricas de performance
- ✅ Contadores de operações
- ✅ Status health checks

---

## 🔧 Configurações

### **Auto-Refresh**
Por padrão, atualiza a cada 5 segundos. Para alterar:

```javascript
// Em app.js, linha ~27
autoRefreshInterval = setInterval(() => {
    // ...
}, 5000); // Altere este valor (em ms)
```

### **Limites de Listagem**
```javascript
// Tasks
const response = await fetch(`${API_URL}/tasks?limit=50`);

// Logs
const response = await fetch(`${API_URL}/logs?limit=100`);
```

### **Filtros de Log**
```python
# Em api_server.py
@app.route('/api/logs')
def get_logs():
    level = request.args.get('level', 'all').upper()
    # Níveis disponíveis: INFO, WARNING, ERROR, DEBUG
```

---

## 📊 Monitoramento e Métricas

### **Logs da API**
Localização: `./logs/api_server.log`

Formato:
```
2025-10-19 14:32:15 [INFO] __main__: ✅ Tarefa criada: #5 - Estudar Python
2025-10-19 14:32:20 [INFO] __main__: 📋 Listando 15 tarefas (filtro: pending)
2025-10-19 14:32:25 [ERROR] __main__: ❌ Erro ao processar: Connection timeout
```

### **Métricas em Tempo Real**
A interface exibe:
- 📋 Tarefas ativas
- ✅ Tarefas concluídas
- 📅 Eventos próximos
- 📝 Total de notas

### **Health Check**
```bash
curl http://localhost:5000/api/status
```

---

## 🐛 Troubleshooting

### **Servidor não inicia**
1. Verifique se a porta 5000 está livre
2. Certifique-se que o ambiente virtual está ativo
3. Verifique logs em `./logs/api_server.log`

### **Interface não carrega**
1. Limpe cache do navegador (Ctrl+Shift+R)
2. Verifique console do navegador (F12)
3. Certifique-se que a API está rodando

### **Tarefas não aparecem**
1. Verifique se `data/tasks.json` existe
2. Confirme permissões de leitura/escrita
3. Veja logs da API

### **Auto-refresh não funciona**
1. Verifique console do navegador
2. Confirme que não há erros de CORS
3. Teste manualmente com botão "Atualizar"

---

## 🔐 Segurança

### **CORS**
Atualmente configurado para desenvolvimento (permite todas as origens).

Para produção:
```python
# Em api_server.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://seu-dominio.com"]
    }
})
```

### **Validação**
- Todos os inputs são sanitizados
- Confirmação para ações destrutivas
- Rate limiting pode ser adicionado

---

## 🚀 Próximos Passos

### **Planejado**
- [ ] Autenticação de usuários
- [ ] Sincronização com Google Calendar
- [ ] Notificações push
- [ ] Exportar tarefas (PDF, CSV)
- [ ] Temas personalizáveis
- [ ] Atalhos de teclado
- [ ] Drag & drop para prioridades
- [ ] Gráficos de produtividade
- [ ] Integração com Notion/Trello
- [ ] API WebSocket para updates em tempo real

---

## 📝 Changelog

### **v2.0.0** (Atual)
- ✅ Interface completamente redesenhada
- ✅ Suporte a calendário
- ✅ Sistema de notas com tags
- ✅ Logs avançados com filtros
- ✅ Dashboard com métricas
- ✅ Modais para criação de items
- ✅ Busca em tempo real
- ✅ Auto-refresh inteligente
- ✅ Logging estruturado na API
- ✅ Novos endpoints (metrics, search)
- ✅ Responsivo mobile-first

### **v1.0.0**
- ✅ Interface básica
- ✅ CRUD de tarefas
- ✅ API REST funcional

---

## 🤝 Contribuindo

Para contribuir com melhorias:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor

Desenvolvido como parte do MCP Server Tools

**Contato:** Veja documentação principal do projeto

---

## 🙏 Agradecimentos

- Claude AI por assistência no desenvolvimento
- Comunidade Flask pela excelente framework
- Contributors do projeto

---

**Última atualização:** 19 de Outubro de 2025
