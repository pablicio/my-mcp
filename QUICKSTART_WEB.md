# ⚡ INÍCIO RÁPIDO - Interface Web

## 🚀 3 Passos para Começar

### 1️⃣ Instalar Flask
```bash
pip install flask flask-cors
```

### 2️⃣ Iniciar Servidor
```bash
start_web_interface.bat
```

### 3️⃣ Abrir Navegador
```
http://localhost:5000
```

---

## ✅ Pronto! Agora você tem:

```
┌─────────────────────────────────────────────────┐
│  🚀 MCP Server Dashboard                        │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Dashboard                                   │
│  ├─ Status: ● Online                           │
│  ├─ Tarefas: 0                                 │
│  ├─ Notas: 0                                   │
│  └─ Ferramentas: 14                            │
│                                                 │
│  [📋 Tarefas] [➕ Nova] [📝 Notas] [📊 Logs]   │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ Nenhuma tarefa encontrada                 │ │
│  │                                           │ │
│  │ Crie sua primeira tarefa →                │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Uso Básico

### Criar Tarefa
1. Clique **"➕ Nova Tarefa"**
2. Preencha:
   - Título: "Estudar Python" ✍️
   - Descrição: "Módulos e pacotes"
   - Prioridade: Alta
3. Clique **"Criar Tarefa"** ✅

### Ver Tarefas
1. Clique **"📋 Tarefas"**
2. Veja todas as tarefas
3. Clique **"✓ Concluir"** para marcar
4. Clique **"🗑️ Deletar"** para remover

### Ver Logs
1. Clique **"📊 Logs"**
2. Veja atividade do servidor
3. Cores indicam tipo:
   - 🔵 INFO
   - 🟢 SUCCESS
   - 🟡 WARNING
   - 🔴 ERROR

---

## 🔄 Atualização Automática

A interface atualiza sozinha a cada 5 segundos! ⏱️

**Você verá:**
- Novas tarefas automaticamente
- Status do servidor em tempo real
- Logs mais recentes
- Estatísticas atualizadas

---

## 💡 Dicas

### Atalhos
- **Enter** no formulário = Criar tarefa
- **Refresh** = F5 no navegador
- **Atualizar dados** = Botão 🔄 em cada aba

### Múltiplas Fontes
Crie tarefas de 3 formas:
1. **Interface Web** → Formulário visual
2. **Claude Desktop** → "crie uma tarefa..."
3. **API direta** → POST /api/tasks

Todas aparecem em todos os lugares! 🎉

---

## 🐛 Problemas?

### Servidor não conecta
```bash
# Verifique se está rodando
# Deve ver: "Running on http://0.0.0.0:5000"

# Reinicie se necessário
Ctrl+C
start_web_interface.bat
```

### "0 tarefas" mas tenho tarefas
```bash
# Reinicie o servidor
Ctrl+C
start_web_interface.bat
```

### Porta 5000 ocupada
```python
# Edite api_server.py, última linha:
app.run(host='0.0.0.0', port=5001)  # Use outra porta
```

---

## 📚 Mais Informações

- **Documentação completa:** [WEB_INTERFACE.md](WEB_INTERFACE.md)
- **Setup detalhado:** [SETUP_COMPLETO.md](SETUP_COMPLETO.md)
- **README principal:** [README.md](README.md)

---

## 🎉 É isso!

**Simples assim:**
```bash
start_web_interface.bat
```

**Resultado:**
- ✅ Dashboard moderno
- ✅ Gerenciamento de tarefas
- ✅ Logs em tempo real
- ✅ Atualização automática

**Divirta-se! 🚀**
