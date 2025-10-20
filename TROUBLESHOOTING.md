# 🔧 Guia de Troubleshooting Visual

## 🚦 Fluxograma de Diagnóstico

```
┌─────────────────────────────────────┐
│   Criar Tarefa via Claude Desktop   │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │  Funcionou?  │
        └──┬────────┬──┘
           │        │
         SIM       NÃO
           │        │
           ▼        ▼
     ┌─────────┐  ┌──────────────────────┐
     │ SUCESSO │  │ Qual erro apareceu?  │
     └─────────┘  └──┬────────────────┬──┘
                     │                │
              "Error executing"   "ID duplicado"
                     │                │
                     ▼                ▼
           ┌──────────────────┐  ┌──────────────┐
           │ PROBLEMA:         │  │ PROBLEMA:    │
           │ Servidor antigo   │  │ Dados antigos│
           └───────┬───────────┘  └──────┬───────┘
                   │                     │
                   ▼                     ▼
           ┌──────────────────┐  ┌──────────────┐
           │ SOLUÇÃO:          │  │ SOLUÇÃO:     │
           │ 1. Fechar Claude  │  │ Executar     │
           │ 2. Aguardar 5seg  │  │ opção [2] do │
           │ 3. Abrir Claude   │  │ menu .bat    │
           └───────────────────┘  └──────────────┘
```

## 📋 Checklist de Validação

### Antes de Reiniciar
```
□ Código modificado em core/server.py
□ Código modificado em modules/tasks/tools.py  
□ Arquivo tasks.json existe em data/
□ Teste manual criado em tests/manual/
```

### Depois de Reiniciar
```
□ Claude Desktop foi fechado completamente
□ Aguardou pelo menos 5 segundos
□ Claude Desktop foi reaberto
□ Tentou criar uma tarefa simples
□ Verificou o arquivo tasks.json
```

### Validação Final
```
□ Tarefa criada com sucesso
□ ID da tarefa é sequencial (1, 2, 3...)
□ Tarefa aparece ao listar
□ Tarefa está no arquivo tasks.json
□ Sem erros no log
```

## 🎯 Cenários Comuns e Soluções

### Cenário 1: "Error executing tool create_task"

**Sintomas:**
```
Error executing tool create_task: 2 validation errors...
args - Field required
kwargs - Field required
```

**Causa:** Servidor MCP usando versão antiga do código

**Solução:**
1. ✅ Fechar Claude Desktop
2. ✅ Aguardar 5-10 segundos
3. ✅ Abrir Claude Desktop
4. ✅ Testar novamente

**Verificação:**
```bash
# Ver logs recentes
cd C:\projetos\IA\mcp\mcp-tools2
type logs\mcp_server.log | more +50
```

---

### Cenário 2: "Tarefa #5 criada" mas arquivo vazio

**Sintomas:**
- Claude diz "Tarefa #5 criada"
- Arquivo tasks.json está vazio ou com contadores baixos
- IDs não batem

**Causa:** Múltiplas instâncias do servidor rodando

**Solução:**
```bash
# Executar test_and_restart.bat
cd C:\projetos\IA\mcp\mcp-tools2
test_and_restart.bat

# Escolher opção [5] - Matar processos Python
# Depois reiniciar Claude Desktop
```

---

### Cenário 3: IDs pulando números (1, 3, 7...)

**Sintomas:**
- IDs não são sequenciais
- Números pulados

**Causa:** Dados antigos no arquivo JSON

**Solução:**
```bash
# Executar test_and_restart.bat
cd C:\projetos\IA\mcp\mcp-tools2
test_and_restart.bat

# Escolher opção [2] - Limpar dados
# Depois reiniciar Claude Desktop
```

---

### Cenário 4: Tarefas somem após reiniciar

**Sintomas:**
- Criar tarefa funciona
- Após reiniciar, tarefas sumiram
- Arquivo tasks.json vazio

**Causa:** Servidor não está salvando no arquivo correto

**Verificação:**
```bash
# Verificar caminho do arquivo
cd C:\projetos\IA\mcp\mcp-tools2
python -c "from config.settings import settings; print(settings.TASKS_DB_PATH)"
```

**Solução:**
- Verificar se o caminho existe
- Verificar permissões de escrita
- Ver logs para erros de I/O

---

### Cenário 5: "Tasks inicializado com 0 tarefas" mas vejo tarefas

**Sintomas:**
- Log diz "0 tarefas"
- Claude mostra tarefas antigas
- Inconsistência

**Causa:** Cache do Claude ou múltiplas instâncias

**Solução:**
1. Limpar dados (opção [2] do menu)
2. Matar processos Python (opção [5])
3. Fechar Claude Desktop
4. Limpar cache do Claude:
   ```
   %APPDATA%\Claude\Cache
   ```
5. Abrir Claude Desktop novamente

## 🔬 Comandos de Diagnóstico

### Ver última atividade do servidor
```bash
cd C:\projetos\IA\mcp\mcp-tools2
type logs\mcp_server.log | findstr "Tarefa criada"
```

### Ver contadores atuais
```bash
cd C:\projetos\IA\mcp\mcp-tools2
python -c "import json; data=json.load(open('data/tasks.json')); print(f'Tasks: {len(data[\"tasks\"])}, Next ID: {data[\"next_task_id\"]}')"
```

### Ver processos Python rodando
```cmd
tasklist | findstr python.exe
```

### Testar módulo diretamente
```bash
cd C:\projetos\IA\mcp\mcp-tools2
python tests\manual\test_tasks_manual.py
```

## 📊 Interpretando os Logs

### ✅ Log Saudável
```
2025-10-19 21:30:00 - TasksTools - INFO - Tasks inicializado com 1 tarefas
2025-10-19 21:30:05 - core.server - INFO - Ferramenta 'tasks_create_task' chamada
2025-10-19 21:30:05 - TasksTools - INFO - Tarefa criada: Minha Tarefa
```

### ❌ Log com Problema
```
2025-10-19 21:30:00 - TasksTools - ERROR - Erro ao carregar dados: ...
2025-10-19 21:30:05 - core.server - ERROR - Erro ao executar ferramenta: ...
```

### ⚠️ Log com Aviso
```
2025-10-19 21:30:00 - TasksTools - WARNING - Arquivo não encontrado, criando novo
```

## 🛠️ Ferramentas de Suporte

### Menu Interativo (test_and_restart.bat)
```
[1] Executar teste manual     - Testa o módulo diretamente
[2] Limpar dados              - Reseta tasks.json
[3] Ver logs do servidor      - Mostra logs recentes
[4] Ver arquivo de tarefas    - Mostra tasks.json
[5] Matar processos Python    - Força reinício
[0] Sair
```

### Script de Teste Manual
```bash
python tests\manual\test_tasks_manual.py
```
Testa:
- Inicialização do módulo
- Criação de tarefas
- Listagem de tarefas
- Busca de tarefas
- Validação de parâmetros

## 🔄 Processo Completo de Reset

Se nada funcionar, siga estes passos:

### 1. Backup (Opcional)
```bash
cd C:\projetos\IA\mcp\mcp-tools2
copy data\tasks.json data\tasks.json.backup
```

### 2. Limpar Tudo
```bash
# Matar processos
taskkill /F /IM python.exe

# Limpar arquivo
echo {"tasks":[],"notes":[],"next_task_id":1,"next_note_id":1} > data\tasks.json

# Limpar logs (opcional)
del logs\mcp_server.log
```

### 3. Verificar Código
```bash
# Ver se modificações estão presentes
findstr "next_task_id" modules\tasks\tools.py
findstr "inspect.signature" core\server.py
```

### 4. Reiniciar Completamente
```bash
1. Fechar Claude Desktop
2. Aguardar 10 segundos
3. Abrir Claude Desktop
4. Aguardar carregar completamente
5. Testar: "crie uma tarefa de teste"
```

### 5. Validar
```bash
# Ver arquivo
type data\tasks.json

# Ver logs
type logs\mcp_server.log | more +50

# Testar diretamente
python tests\manual\test_tasks_manual.py
```

## 📞 Quando Pedir Ajuda

Se após todos os passos ainda não funcionar, documente:

1. **O que tentou:**
   - Listar todos os passos executados

2. **Logs relevantes:**
   ```bash
   type logs\mcp_server.log | more +50
   ```

3. **Conteúdo do arquivo:**
   ```bash
   type data\tasks.json
   ```

4. **Versão do Python:**
   ```bash
   python --version
   ```

5. **Processos rodando:**
   ```bash
   tasklist | findstr python.exe
   ```

6. **Erro exato:**
   - Copiar mensagem de erro completa

## ✅ Checklist Final de Sucesso

Você saberá que tudo está funcionando quando:

```
✅ Comando "crie uma tarefa" funciona sem erros
✅ Comando "liste minhas tarefas" mostra as tarefas
✅ Arquivo tasks.json está atualizado
✅ IDs são sequenciais (1, 2, 3, 4...)
✅ Logs mostram "Tarefa criada: ..."
✅ Não há mensagens de ERROR nos logs
✅ Tarefas persistem após reiniciar Claude Desktop
✅ Teste manual passa sem erros
```

---

**Última Atualização:** 19 de Outubro de 2025  
**Versão:** 1.0.0  
**Status:** ✅ Correções aplicadas - Aguardando reinicialização
