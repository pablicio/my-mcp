# 🧪 Guia de Testes - MCP Server Pessoal

## 📋 Visão Geral

Este documento descreve como testar o MCP Server Pessoal para garantir que está funcionando corretamente.

---

## 🚀 Teste Rápido (5 minutos)

### 1. Teste Automatizado

```bash
# Execute o script de teste
python test_server.py
```

**Saída esperada:**
```
============================================================
🧪 TESTE DO MCP SERVER PESSOAL
============================================================

📦 Teste 1: Verificando importações...
   ✅ Todas as importações OK

⚙️  Teste 2: Verificando configurações...
   📁 Diretórios permitidos: 2
      ✅ C:\Users\User\Documents
      ✅ C:\Users\User\Desktop

🚀 Teste 5: Inicializando servidor...
   ✅ Servidor inicializado

============================================================
📊 RESUMO DOS TESTES
============================================================

✅ Todos os testes passaram! Servidor pronto para uso.
```

### 2. Teste Manual do Servidor

```bash
# Iniciar o servidor
python main.py

# Você deve ver:
# ✅ Servidor MCP inicializado com sucesso!
```

### 3. Teste no Claude Desktop

1. **Reinicie** o Claude Desktop completamente
2. Abra uma **nova conversa**
3. Digite um comando de teste:

```
Claude, liste os arquivos na minha pasta Documents
```

**Resultado esperado:** Claude deve listar os arquivos do seu diretório Documents.

---

## 🔍 Testes Detalhados

### Teste 1: Configuração

```bash
# Verificar configurações
python -c "from config.settings import settings; import json; print(json.dumps(settings.dict(), indent=2, default=str))"
```

**Verificar:**
- ✅ `ALLOWED_DIRECTORIES` contém seus diretórios
- ✅ Todos os caminhos existem
- ✅ `LOG_LEVEL` está correto

### Teste 2: Filesystem Module

**Comandos no Claude:**

```
# Teste 1: Listar diretório
Liste os arquivos na pasta Documents

# Teste 2: Ler arquivo (substitua por arquivo real)
Leia o arquivo README.md

# Teste 3: Criar arquivo
Crie um arquivo teste_mcp.txt com o conteúdo "MCP Server funcionando!"

# Teste 4: Buscar arquivos
Procure arquivos .txt na pasta Documents

# Teste 5: Info de arquivo
Mostre detalhes do arquivo teste_mcp.txt
```

**Resultados esperados:**
- ✅ Lista de arquivos/diretórios
- ✅ Conteúdo do arquivo
- ✅ Confirmação de criação
- ✅ Lista de arquivos encontrados
- ✅ Informações detalhadas

### Teste 3: Tasks Module

**Comandos no Claude:**

```
# Teste 1: Criar tarefa
Crie uma tarefa: "Testar MCP Server" com prioridade alta

# Teste 2: Listar tarefas
Mostre minhas tarefas pendentes

# Teste 3: Completar tarefa
Marque a tarefa #1 como concluída

# Teste 4: Criar nota
Crie uma nota: "MCP funcionando" com o conteúdo "Testes realizados com sucesso" e tags teste,mcp

# Teste 5: Listar notas
Mostre minhas notas recentes
```

**Resultados esperados:**
- ✅ Tarefa criada com ID
- ✅ Lista de tarefas formatada
- ✅ Tarefa marcada como concluída 🎉
- ✅ Nota criada
- ✅ Lista de notas

### Teste 4: Segurança

**Testes que DEVEM FALHAR (comportamento esperado):**

```
# Teste 1: Path traversal (deve falhar)
Leia o arquivo ../../etc/passwd

# Teste 2: Diretório não permitido (deve falhar)
Liste arquivos em C:\Windows\System32

# Teste 3: Arquivo muito grande (deve falhar se >10MB)
[Tentar ler arquivo maior que 10MB]
```

**Resultados esperados:**
- ❌ "Erro: Acesso negado"
- ❌ "Erro: Diretório não permitido"
- ❌ "Erro: Arquivo muito grande"

---

## 🧪 Testes Unitários

### Executar Todos os Testes

```bash
# Executar com pytest
python -m pytest tests/ -v

# Com coverage
python -m pytest tests/ --cov=. --cov-report=html

# Ver relatório de coverage
# Abra htmlcov/index.html no navegador
```

### Executar Testes Específicos

```bash
# Apenas filesystem
python -m pytest tests/test_filesystem.py -v

# Apenas tasks
python -m pytest tests/test_tasks.py -v

# Apenas segurança
python -m pytest tests/test_security.py -v

# Teste específico
python -m pytest tests/test_tasks.py::test_create_task -v
```

### Saída Esperada

```
tests/test_filesystem.py::test_is_available PASSED
tests/test_filesystem.py::test_get_tools PASSED
tests/test_tasks.py::test_create_task PASSED
tests/test_tasks.py::test_list_tasks PASSED
tests/test_security.py::test_sanitize_filename PASSED

==================== 15 passed in 2.34s ====================
```

---

## 🔧 Testes de Integração

### Teste Completo do Workflow

```bash
# 1. Iniciar servidor em uma janela
python main.py

# 2. Em outra janela, monitorar logs
tail -f logs/mcp_server.log  # Linux/Mac
Get-Content logs/mcp_server.log -Wait  # Windows

# 3. No Claude Desktop, executar sequência completa:
```

**Sequência de testes no Claude:**

```
1. Liste arquivos na pasta Documents
2. Crie arquivo teste.txt com "Hello MCP"
3. Leia o arquivo teste.txt
4. Crie tarefa: "Revisar logs" prioridade alta
5. Mostre minhas tarefas
6. Marque tarefa #1 como concluída
7. Crie nota: "Teste completo" conteúdo "Tudo funcionou"
8. Delete o arquivo teste.txt (com confirmação)
```

**Verificar logs para:**
- ✅ Cada operação está logada
- ✅ Não há erros ou exceções
- ✅ Timestamps corretos
- ✅ Informações de segurança

---

## 📊 Checklist de Testes

### Antes de Usar em Produção

- [ ] `python test_server.py` passa todos os testes
- [ ] `python -m pytest tests/` passa todos os testes
- [ ] Servidor inicia sem erros
- [ ] Claude Desktop reconhece o servidor
- [ ] Operações de leitura funcionam
- [ ] Operações de escrita funcionam
- [ ] Segurança impede acesso não autorizado
- [ ] Logs são gerados corretamente
- [ ] Tarefas são persistidas
- [ ] Performance é aceitável (<1s por operação)

### Testes de Performance

```python
# Teste de performance simples
import time
import asyncio
from modules.filesystem.tools import FilesystemTools

async def test_performance():
    fs = FilesystemTools()
    await fs.initialize()
    
    start = time.time()
    result = await fs.list_directory(".")
    elapsed = time.time() - start
    
    print(f"Tempo: {elapsed:.2f}s")
    assert elapsed < 1.0, "Operação muito lenta"

asyncio.run(test_performance())
```

---

## 🐛 Debugging de Testes

### Testes Falham?

```bash
# 1. Ativar modo debug
echo "LOG_LEVEL=DEBUG" >> .env

# 2. Executar teste individual com traceback completo
python -m pytest tests/test_filesystem.py -vv --tb=long

# 3. Ver logs detalhados
cat logs/mcp_server.log | tail -n 100
```

### Claude não vê o servidor?

```bash
# 1. Verificar se servidor está rodando
ps aux | grep main.py  # Linux/Mac
tasklist | findstr python  # Windows

# 2. Verificar configuração do Claude
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json  # Mac
type %APPDATA%\Claude\claude_desktop_config.json  # Windows

# 3. Testar conexão manualmente
curl http://localhost:8080  # Se o servidor expor HTTP
```

### Erros de Permissão?

```bash
# Verificar permissões dos diretórios
ls -la /caminho/para/diretorio  # Linux/Mac

# Adicionar permissões se necessário
chmod -R 755 /caminho/para/diretorio  # Linux/Mac
```

---

## 📈 Monitoramento Contínuo

### Durante o Uso

```bash
# Terminal 1: Servidor
python main.py

# Terminal 2: Monitorar logs
tail -f logs/mcp_server.log | grep -i error

# Terminal 3: Monitorar recursos
htop  # ou top
```

### Métricas a Observar

- 🔍 **Latência**: Operações devem ser <1s
- 💾 **Memória**: Uso estável, sem memory leaks
- 📝 **Logs**: Sem erros recorrentes
- 🔒 **Segurança**: Todas tentativas inválidas são bloqueadas

---

## ✅ Testes Aprovados

Se todos os testes passarem, você verá:

```
✅ Testes automatizados: PASS
✅ Servidor inicializa: PASS
✅ Claude Desktop conecta: PASS
✅ Filesystem funciona: PASS
✅ Tasks funciona: PASS
✅ Segurança ativa: PASS
✅ Logs gerados: PASS

🎉 MCP Server aprovado para uso!
```

---

## 🆘 Ajuda

Se algum teste falhar:

1. Veja `logs/mcp_server.log`
2. Execute `python test_server.py` para diagnóstico
3. Consulte `GUIA_COMPLETO.md` seção Troubleshooting
4. Verifique `QUICK_REFERENCE.md` para comandos rápidos

---

**Boa sorte com os testes! 🚀**
