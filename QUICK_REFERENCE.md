# ⚡ Referência Rápida - MCP Server Pessoal

## 🚀 Instalação e Execução

```bash
# Setup completo
python setup.py

# Iniciar servidor
python main.py

# Modo debug
DEBUG=true python main.py
```

## 📁 Comandos Filesystem

| Comando | Exemplo Claude |
|---------|----------------|
| Listar | `Liste arquivos em Documents` |
| Ler | `Leia o arquivo README.md` |
| Criar | `Crie arquivo test.py com Hello World` |
| Buscar | `Procure arquivos .txt em Documents` |
| Info | `Mostre detalhes do arquivo config.json` |
| Deletar | `Delete o arquivo old.txt` (requer confirmação) |

## ✅ Comandos de Tarefas

| Comando | Exemplo Claude |
|---------|----------------|
| Criar | `Crie tarefa: Revisar docs (alta prioridade)` |
| Listar | `Mostre minhas tarefas pendentes` |
| Completar | `Marque tarefa #3 como concluída` |
| Buscar | `Encontre tarefas com 'python'` |
| Deletar | `Delete tarefa #5` (requer confirmação) |

## 📝 Comandos de Notas

| Comando | Exemplo Claude |
|---------|----------------|
| Criar | `Crie nota: Ideias do projeto com tags brainstorm,urgent` |
| Listar | `Mostre minhas notas recentes` |

## 📅 Google Calendar (se configurado)

| Comando | Exemplo Claude |
|---------|----------------|
| Criar evento | `Adicione 'Reunião' amanhã às 14h` |
| Listar | `Quais meus compromissos hoje?` |
| Buscar | `Encontre eventos com 'médico'` |

## 🔧 Configuração

### Locais dos Arquivos

**Windows:**
- Config Claude: `%APPDATA%\Claude\claude_desktop_config.json`
- .env: `C:\projetos\IA\mcp\mcp-tools2\.env`

**Mac:**
- Config Claude: `~/Library/Application Support/Claude/claude_desktop_config.json`
- .env: `/caminho/projeto/.env`

**Linux:**
- Config Claude: `~/.config/Claude/claude_desktop_config.json`
- .env: `/caminho/projeto/.env`

### Variáveis .env Principais

```env
# Diretórios (caminhos absolutos separados por vírgula)
ALLOWED_DIRECTORIES=C:\Users\User\Documents,C:\projetos

# Logs
LOG_LEVEL=INFO  # DEBUG para mais detalhes
DEBUG=false

# Google Calendar (opcional)
# GOOGLE_CLIENT_ID=...
# GOOGLE_CLIENT_SECRET=...
```

## 🐛 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Claude não vê servidor | 1. Reinicie Claude Desktop<br>2. Verifique claude_desktop_config.json<br>3. Teste: `python main.py` |
| Erro de importação | `pip install -r requirements.txt` |
| Diretório negado | Adicione em ALLOWED_DIRECTORIES (.env) |
| Servidor não inicia | Verifique logs: `logs/mcp_server.log` |

## 📊 Verificações

```bash
# Testar configuração
python -c "from config.settings import settings; print(settings.dict())"

# Ver diretórios permitidos
python -c "from config.settings import settings; print(settings.ALLOWED_DIRECTORIES)"

# Executar testes
python -m pytest tests/ -v

# Ver logs em tempo real (Linux/Mac)
tail -f logs/mcp_server.log

# Ver logs em tempo real (Windows PowerShell)
Get-Content logs/mcp_server.log -Wait
```

## 🔒 Segurança

- ✅ Acesso apenas a diretórios configurados
- ✅ Validação de caminhos (sem `../`)
- ✅ Limite de 10MB por arquivo
- ✅ Timeout de 30s por operação
- ✅ Todas operações são logadas

## 📚 Arquivos Importantes

- `main.py` - Inicia o servidor
- `.env` - Suas configurações
- `logs/mcp_server.log` - Logs de operações
- `data/tasks.json` - Suas tarefas
- `README.md` - Documentação completa
- `GUIA_COMPLETO.md` - Guia detalhado

## 🆘 Comandos de Emergência

```bash
# Parar servidor
Ctrl+C

# Limpar logs
rm logs/mcp_server.log  # Linux/Mac
del logs\mcp_server.log  # Windows

# Resetar tarefas
rm data/tasks.json  # Linux/Mac
del data\tasks.json  # Windows

# Reinstalar tudo
pip install -r requirements.txt --force-reinstall
python setup.py
```

## 💡 Dicas

1. **Sempre use caminhos absolutos** em ALLOWED_DIRECTORIES
2. **Reinicie Claude Desktop** após mudanças na config
3. **Verifique logs** quando algo não funcionar
4. **Teste no terminal** antes de usar no Claude: `python main.py`
5. **Backup** de data/tasks.json regularmente

---

**⚡ Atalho:** Mantenha este arquivo aberto para referência rápida!
