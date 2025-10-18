# 🎯 Como Executar, Testar e Conhecer o MCP Server Pessoal

## 📋 Índice

1. [Primeira Execução](#-primeira-execução)
2. [Testando a Ferramenta](#-testando-a-ferramenta)
3. [Conhecendo as Funcionalidades](#-conhecendo-as-funcionalidades)
4. [Casos de Uso Práticos](#-casos-de-uso-práticos)
5. [Monitoramento e Logs](#-monitoramento-e-logs)
6. [Solução de Problemas](#-solução-de-problemas)

---

## 🚀 Primeira Execução

### Passo 1: Preparar o Ambiente

```bash
# Navegue até o diretório do projeto
cd C:\projetos\IA\mcp\mcp-tools2

# Verifique se Python está instalado (precisa ser 3.9+)
python --version
```

### Passo 2: Executar o Setup

```bash
# Execute o setup automatizado
python setup.py
```

**O que o setup faz:**
- ✅ Verifica Python 3.9+
- ✅ Instala dependências do `requirements.txt`
- ✅ Cria arquivo `.env` com suas configurações
- ✅ Pede seus diretórios permitidos
- ✅ Configura o Claude Desktop automaticamente
- ✅ Cria pastas `logs/` e `data/`
- ✅ Testa a instalação

**Durante o setup, você será perguntado:**
```
📁 Configuração de diretórios permitidos:
   Informe os caminhos absolutos separados por vírgula
   Exemplo: C:\Users\Usuario\Documents,C:\Users\Usuario\Desktop
   Diretórios (Enter para padrão): _
```

**Digite seus diretórios**, por exemplo:
```
C:\Users\SeuNome\Documents,C:\Users\SeuNome\Desktop,C:\projetos
```

### Passo 3: Iniciar o Servidor

```bash
# Iniciar o servidor
python main.py
```

**Você deve ver:**
```
============================================================
🚀 MCP SERVER PESSOAL v1.0.0
============================================================
🌐 Host: localhost:8080
🐛 Debug: Disabled
Carregando módulo filesystem...
Módulo filesystem carregado com sucesso
Carregando módulo tasks...
Módulo tasks carregado com sucesso
✅ Servidor MCP inicializado com sucesso!
🔧 Para parar: Ctrl+C
📊 Logs: ./logs/mcp_server.log
```

**Se ver isso, está funcionando! 🎉**

### Passo 4: Reiniciar o Claude Desktop

**IMPORTANTE:** Você DEVE reiniciar o Claude Desktop completamente:

1. Feche o Claude Desktop (feche todas as janelas)
2. Abra novamente o Claude Desktop
3. Aguarde carregar completamente

---

## 🧪 Testando a Ferramenta

### Teste Automático

Antes de usar no Claude, execute o teste automatizado:

```bash
# Em outro terminal (mantendo o servidor rodando)
python test_server.py
```

**Resultado esperado:**
```
============================================================
🧪 TESTE DO MCP SERVER PESSOAL
============================================================

📦 Teste 1: Verificando importações...
   ✅ Todas as importações OK

⚙️  Teste 2: Verificando configurações...
   📁 Diretórios permitidos: 3
      ✅ C:\Users\Usuario\Documents
      ✅ C:\Users\Usuario\Desktop
      ✅ C:\projetos

🔧 Teste 4: Testando módulos...
   📁 Filesystem: ✅ Disponível
      Ferramentas: 7
   ✅ Tasks: ✅ Disponível
      Ferramentas: 7

🚀 Teste 5: Inicializando servidor...
   ✅ Servidor inicializado
      Módulos carregados: 2
      Ferramentas: 14

============================================================
📊 RESUMO DOS TESTES
============================================================

✅ Todos os testes passaram! Servidor pronto para uso.
```

### Teste Manual no Claude Desktop

Abra uma nova conversa no Claude e teste cada funcionalidade:

#### Teste 1: Listar Arquivos

**Digite no Claude:**
```
Liste os arquivos na minha pasta Documents
```

**Resultado esperado:**
```
Conteúdo de C:\Users\Usuario\Documents:
📄 projeto.docx (52,341 bytes)
📄 notas.txt (1,234 bytes)
📁 trabalho/
📁 pessoal/
...
```

#### Teste 2: Criar Arquivo

**Digite no Claude:**
```
Crie um arquivo chamado teste_mcp.txt com o conteúdo "MCP Server está funcionando perfeitamente!"
```

**Resultado esperado:**
```
Arquivo C:\Users\Usuario\Documents\teste_mcp.txt salvo com sucesso (49 caracteres)
```

#### Teste 3: Ler Arquivo

**Digite no Claude:**
```
Leia o arquivo teste_mcp.txt que acabamos de criar
```

**Resultado esperado:**
```
MCP Server está funcionando perfeitamente!
```

#### Teste 4: Criar Tarefa

**Digite no Claude:**
```
Crie uma tarefa: "Explorar funcionalidades do MCP Server" com prioridade alta
```

**Resultado esperado:**
```
Tarefa #1 'Explorar funcionalidades do MCP Server' criada com sucesso
```

#### Teste 5: Listar Tarefas

**Digite no Claude:**
```
Mostre minhas tarefas pendentes
```

**Resultado esperado:**
```
Tarefas (pending):
⏳ #1 🔴 Explorar funcionalidades do MCP Server
```

#### Teste 6: Completar Tarefa

**Digite no Claude:**
```
Marque a tarefa #1 como concluída
```

**Resultado esperado:**
```
Tarefa #1 'Explorar funcionalidades do MCP Server' marcada como concluída! 🎉
```

---

## 🎓 Conhecendo as Funcionalidades

### 1. Sistema de Arquivos

O módulo Filesystem permite que o Claude interaja com seus arquivos de forma segura.

**Ferramentas disponíveis:**

| Ferramenta | Descrição | Exemplo |
|------------|-----------|---------|
| `read_file` | Lê conteúdo de arquivo | "Leia arquivo.txt" |
| `write_file` | Cria/sobrescreve arquivo | "Crie config.json com {...}" |
| `list_directory` | Lista conteúdo de pasta | "Liste arquivos em Documents" |
| `search_files` | Busca arquivos por padrão | "Procure *.py em projetos" |
| `file_info` | Informações detalhadas | "Info de arquivo.pdf" |
| `delete_file` | Remove arquivo (com confirmação) | "Delete old.txt" |
| `create_directory` | Cria novo diretório | "Crie pasta backup" |

**Recursos de Segurança:**
- ✅ Acesso apenas a diretórios configurados em `.env`
- ✅ Bloqueio de path traversal (`../`)
- ✅ Limite de 10MB por arquivo
- ✅ Validação de nomes de arquivo

**Exemplos práticos:**

```
# Organizando arquivos
"Procure todos arquivos .pdf na pasta Documents e me mostre"

# Lendo código
"Leia o arquivo main.py e me explique o que ele faz"

# Criando documentação
"Crie um arquivo CHANGELOG.md listando as mudanças recentes"

# Analisando logs
"Leia o arquivo error.log e me diga os principais erros"
```

### 2. Sistema de Tarefas

Gerencie suas tarefas e notas diretamente com o Claude.

**Ferramentas disponíveis:**

| Ferramenta | Descrição | Exemplo |
|------------|-----------|---------|
| `create_task` | Cria nova tarefa | "Tarefa: Revisar docs" |
| `list_tasks` | Lista tarefas | "Mostre tarefas pendentes" |
| `complete_task` | Marca como concluída | "Complete tarefa #3" |
| `delete_task` | Remove tarefa | "Delete tarefa #5" |
| `create_note` | Cria nota | "Nota: Ideias projeto" |
| `list_notes` | Lista notas | "Mostre minhas notas" |
| `search_tasks` | Busca tarefas | "Encontre 'python'" |

**Recursos:**
- 🎯 Prioridades: alta, média, baixa
- ✅ Status: pendente, concluída
- 📅 Datas de prazo
- 🏷️ Tags para notas
- 💾 Persistência em JSON

**Exemplos práticos:**

```
# Gerenciamento de projeto
"Crie 3 tarefas para o projeto: 1) Revisar código, 2) Atualizar docs, 3) Testar features"

# Acompanhamento
"Liste minhas tarefas ordenadas por prioridade"

# Brainstorming
"Crie uma nota com minhas ideias para melhorias no projeto, tags: brainstorm, futuro"

# Revisão semanal
"Mostre todas as tarefas que completei esta semana"
```

### 3. Google Calendar (Opcional)

Integração com sua agenda do Google.

**Ferramentas disponíveis:**

| Ferramenta | Descrição | Exemplo |
|------------|-----------|---------|
| `create_event` | Cria evento | "Evento: Reunião amanhã 14h" |
| `list_events` | Lista compromissos | "Meus eventos hoje" |
| `search_events` | Busca eventos | "Encontre 'médico'" |

**Para configurar:**
1. Obtenha credenciais OAuth2 no Google Cloud Console
2. Configure `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET` no `.env`
3. Na primeira vez, você será redirecionado para autorizar

---

## 💼 Casos de Uso Práticos

### Caso 1: Desenvolvedor de Software

```
# Analisando projeto
"Liste todos arquivos Python no diretório projetos/meu-app"

# Revisando código
"Leia o arquivo auth.py e sugira melhorias de segurança"

# Criando documentação
"Crie um README.md para o projeto com base nos arquivos que você viu"

# Gerenciando bugs
"Crie tarefas para os 5 bugs mais críticos que encontramos"

# Organizando sprint
"Liste minhas tarefas de desenvolvimento ordenadas por prioridade"
```

### Caso 2: Estudante

```
# Organizando matérias
"Crie tarefas para estudar: Matemática (segunda), Física (terça), Química (quarta)"

# Anotações
"Crie nota com resumo da aula de hoje, tags: aula, importante"

# Revisão
"Mostre minhas notas com tag 'prova'"

# Agenda
"Crie evento: Prova de Matemática na próxima sexta às 10h"

# Pesquisa
"Procure arquivos PDF sobre 'física quântica' na minha pasta Downloads"
```

### Caso 3: Profissional/Escritório

```
# Gerenciamento de documentos
"Liste todos documentos Word na pasta Contratos"

# Backup de informações
"Crie arquivo backup_contacts.txt com lista de contatos importantes"

# Agenda do dia
"Quais são meus compromissos de hoje?"

# Tarefas urgentes
"Crie tarefa de alta prioridade: Enviar relatório até 17h"

# Busca rápida
"Encontre arquivos contendo 'proposta' no nome em Documents"
```

### Caso 4: Pesquisador

```
# Organização de papers
"Liste todos PDFs na pasta Research ordenados por data"

# Anotações de leitura
"Crie nota: Resumo do paper sobre IA, tags: research, ai, importante"

# Cronograma de pesquisa
"Crie tarefas para as etapas da pesquisa com prazos"

# Análise de dados
"Leia o arquivo results.csv e me dê um resumo dos dados"
```

---

## 📊 Monitoramento e Logs

### Ver Logs em Tempo Real

**Linux/Mac:**
```bash
tail -f logs/mcp_server.log
```

**Windows PowerShell:**
```powershell
Get-Content logs/mcp_server.log -Wait
```

**Windows Command Prompt:**
```cmd
type logs\mcp_server.log
```

### Interpretar os Logs

```
2025-10-18 14:23:45 - INFO - Servidor MCP inicializado
2025-10-18 14:24:10 - INFO - Arquivo lido: C:\Users\User\Documents\test.txt
2025-10-18 14:24:15 - INFO - Tarefa criada: Revisar código
2025-10-18 14:24:20 - WARNING - Arquivo deletado: C:\Users\User\Documents\old.txt
2025-10-18 14:24:25 - ERROR - Acesso negado: C:\Windows\system.ini
```

**Níveis de log:**
- `INFO` - Operações normais
- `WARNING` - Avisos (deletar arquivos, etc)
- `ERROR` - Erros (acesso negado, arquivo não encontrado)
- `DEBUG` - Informações detalhadas (ative com `DEBUG=true`)

### Ativar Modo Debug

```bash
# No .env
LOG_LEVEL=DEBUG

# Ou temporariamente
DEBUG=true python main.py
```

---

## 🔧 Solução de Problemas

### Problema: Claude não reconhece o servidor

**Sintoma:** Claude responde normalmente mas não usa as ferramentas

**Soluções:**

1. **Reinicie o Claude Desktop completamente**
   ```
   - Feche TODAS as janelas do Claude
   - Aguarde 5 segundos
   - Abra novamente
   ```

2. **Verifique se o servidor está rodando**
   ```bash
   # Deve mostrar o processo Python
   # Windows
   tasklist | findstr python
   
   # Linux/Mac
   ps aux | grep main.py
   ```

3. **Verifique a configuração do Claude**
   ```bash
   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json
   
   # Mac
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Linux
   cat ~/.config/Claude/claude_desktop_config.json
   ```

4. **Teste manualmente**
   ```bash
   python main.py
   # Deve iniciar sem erros
   ```

### Problema: "Diretório não permitido"

**Sintoma:** Claude diz que não pode acessar o diretório

**Soluções:**

1. **Verifique o .env**
   ```bash
   # Ver diretórios configurados
   python -c "from config.settings import settings; print(settings.ALLOWED_DIRECTORIES)"
   ```

2. **Use caminhos absolutos**
   ```
   ❌ Errado: ALLOWED_DIRECTORIES=Documents,Desktop
   ✅ Correto: ALLOWED_DIRECTORIES=C:\Users\Usuario\Documents,C:\Users\Usuario\Desktop
   ```

3. **Verifique que o diretório existe**
   ```bash
   # Windows
   dir "C:\Users\Usuario\Documents"
   
   # Linux/Mac
   ls -la /home/usuario/Documents
   ```

4. **Reinicie o servidor** após mudar `.env`

### Problema: Erro de importação

**Sintoma:** `ModuleNotFoundError` ou `ImportError`

**Solução:**

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar Python
python --version  # Deve ser 3.9+

# Verificar instalação
python -c "import mcp; print('OK')"
```

### Problema: Servidor não inicia

**Sintoma:** Erro ao executar `python main.py`

**Soluções:**

1. **Ver erro completo**
   ```bash
   python main.py
   # Leia a mensagem de erro
   ```

2. **Verificar porta em uso**
   ```bash
   # Windows
   netstat -ano | findstr :8080
   
   # Linux/Mac
   lsof -i :8080
   ```

3. **Mudar porta se necessário**
   ```env
   # No .env
   PORT=8081
   ```

4. **Verificar permissões**
   - Certifique-se de ter permissão para criar pastas `logs/` e `data/`

---

## ✅ Checklist de Verificação

Antes de usar em produção:

- [ ] `python test_server.py` passa todos os testes
- [ ] `python main.py` inicia sem erros
- [ ] Claude Desktop reconhece o servidor
- [ ] Consegue listar arquivos
- [ ] Consegue criar arquivos
- [ ] Consegue criar tarefas
- [ ] Logs estão sendo gerados
- [ ] Diretórios permitidos estão corretos
- [ ] Segurança está ativa (tente acessar `/etc/passwd`)

---

## 🎉 Conclusão

Agora você está pronto para usar o MCP Server Pessoal!

**Próximos passos:**
1. Explore as funcionalidades no Claude
2. Adapte para seu workflow
3. Adicione novos módulos se necessário
4. Compartilhe casos de uso interessantes

**Recursos adicionais:**
- 📖 [README.md](README.md) - Visão geral
- 📚 [GUIA_COMPLETO.md](GUIA_COMPLETO.md) - Documentação detalhada
- ⚡ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Referência rápida
- 🧪 [TESTES.md](TESTES.md) - Guia de testes

---

**Aproveite o seu MCP Server! 🚀**
