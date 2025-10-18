# ❓ FAQ - Perguntas Frequentes

## 📋 Índice

- [Instalação e Configuração](#instalação-e-configuração)
- [Uso e Funcionalidades](#uso-e-funcionalidades)
- [Problemas Comuns](#problemas-comuns)
- [Segurança](#segurança)
- [Desenvolvimento](#desenvolvimento)

---

## Instalação e Configuração

### P: Qual versão do Python preciso?

**R:** Python 3.9 ou superior. Verifique com:
```bash
python --version
```

### P: O setup é obrigatório?

**R:** Não é obrigatório, mas é **altamente recomendado**. O setup automatiza tudo e evita erros comuns. Se preferir manual, siga o [GUIA_COMPLETO.md](GUIA_COMPLETO.md).

### P: Preciso reiniciar o Claude Desktop?

**R:** **SIM!** Sempre que:
- Instalar/configurar o servidor pela primeira vez
- Mudar configurações no `claude_desktop_config.json`
- O Claude não reconhecer o servidor

**Reinicie COMPLETAMENTE** (feche todas as janelas).

### P: Onde fica o arquivo de configuração do Claude Desktop?

**R:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

### P: Posso usar diretórios relativos no .env?

**R:** **NÃO!** Use sempre caminhos absolutos:
```env
❌ ERRADO: ALLOWED_DIRECTORIES=Documents,Desktop
✅ CORRETO: ALLOWED_DIRECTORIES=C:\Users\Usuario\Documents,C:\Users\Usuario\Desktop
```

### P: Como adicionar mais diretórios permitidos depois?

**R:**
1. Edite `.env` e adicione o novo caminho
2. Reinicie o servidor (`Ctrl+C` e `python main.py`)
3. Teste no Claude

---

## Uso e Funcionalidades

### P: Como sei se o servidor está funcionando?

**R:** Execute `python test_server.py` ou veja se o servidor iniciou sem erros ao executar `python main.py`.

### P: O Claude não está usando as ferramentas. Por quê?

**R:** Verifique:
1. Servidor está rodando? (`python main.py`)
2. Claude Desktop foi reiniciado?
3. Configuração está correta? (veja arquivo config do Claude)
4. Logs mostram erros? (`logs/mcp_server.log`)

### P: Posso usar o servidor com múltiplas conversas do Claude?

**R:** Sim! O servidor atende todas as conversas do Claude Desktop simultaneamente.

### P: As tarefas ficam salvas entre sessões?

**R:** Sim! Tarefas e notas são salvas em `data/tasks.json` e persistem entre reinicializações.

### P: Como criar uma tarefa com prazo?

**R:** No Claude:
```
Crie tarefa: "Entregar relatório" com prioridade alta e prazo para 2025-10-25
```

### P: Posso deletar arquivos?

**R:** Sim, mas o sistema sempre pede confirmação:
```
Claude: "Delete o arquivo old.txt"
Resposta: "ATENÇÃO: Deletar permanentemente? Use confirm=True"
Claude: "Delete o arquivo old.txt com confirmação"
```

### P: Como procurar arquivos em subpastas?

**R:**
```
Procure arquivos .pdf recursivamente na pasta Documents
```

### P: Posso ler arquivos grandes?

**R:** Limite padrão é 10MB. Para arquivos maiores, você pode:
1. Aumentar `MAX_FILE_SIZE` no `.env`
2. Ou pedir ao Claude para ler em partes

---

## Problemas Comuns

### P: "ModuleNotFoundError: No module named 'mcp'"

**R:**
```bash
pip install -r requirements.txt --force-reinstall
```

### P: "Erro: Acesso negado ao caminho..."

**R:** O caminho não está em `ALLOWED_DIRECTORIES`:
1. Verifique `.env`
2. Adicione o diretório necessário
3. Use caminho absoluto
4. Reinicie o servidor

### P: "Erro: Diretório não encontrado"

**R:** O diretório em `ALLOWED_DIRECTORIES` não existe:
1. Verifique se digitou corretamente
2. Verifique se o diretório realmente existe
3. Use caminho absoluto

### P: Servidor não inicia - "Address already in use"

**R:** A porta 8080 está em uso:
```env
# No .env, mude a porta
PORT=8081
```

### P: Como ver erros detalhados?

**R:**
```bash
# Ativar debug no .env
LOG_LEVEL=DEBUG
DEBUG=true

# Ou temporariamente
DEBUG=true python main.py

# Ver logs
tail -f logs/mcp_server.log  # Linux/Mac
Get-Content logs/mcp_server.log -Wait  # Windows
```

### P: O servidor trava/fica lento

**R:**
1. Verifique os logs por erros
2. Limite operações recursivas
3. Evite arquivos muito grandes
4. Reinicie o servidor

### P: "Permission denied" ao criar arquivo

**R:**
1. Verifique permissões do diretório
2. Execute como usuário com permissões adequadas
3. No Windows, execute como administrador se necessário

---

## Segurança

### P: É seguro usar este servidor?

**R:** Sim! O servidor implementa várias camadas de segurança:
- ✅ Allowlist de diretórios
- ✅ Validação de paths (sem `../`)
- ✅ Limite de tamanho
- ✅ Timeout de operações
- ✅ Logging completo

Mas **você é responsável por**:
- Configurar apenas diretórios necessários
- Não expor o servidor na rede
- Manter o acesso local (localhost)

### P: O Claude pode acessar qualquer arquivo do meu computador?

**R:** **NÃO!** Apenas os diretórios que você configurar em `ALLOWED_DIRECTORIES`. Tentativas de acesso fora são bloqueadas.

### P: O que acontece se tentar acessar C:\Windows?

**R:** Se não estiver em `ALLOWED_DIRECTORIES`, será bloqueado:
```
Erro: Acesso negado ao caminho C:\Windows\system32
```

### P: Posso compartilhar meu servidor?

**R:** **NÃO é recomendado**. Este servidor é para uso local pessoal. Para compartilhar, você precisaria adicionar autenticação e outras medidas de segurança.

### P: Os logs contêm informações sensíveis?

**R:** Os logs registram operações (arquivos lidos/escritos, tarefas criadas), mas não o conteúdo. Revise `logs/mcp_server.log` se tiver dúvidas.

### P: Como proteger dados sensíveis?

**R:**
1. Não coloque diretórios sensíveis em `ALLOWED_DIRECTORIES`
2. Use criptografia de disco se necessário
3. Revise logs regularmente
4. Backup regularmente de `data/`

---

## Desenvolvimento

### P: Como adicionar um novo módulo?

**R:** Veja exemplo em [GUIA_COMPLETO.md](GUIA_COMPLETO.md#desenvolvimento). Basicamente:
1. Crie pasta em `modules/`
2. Implemente classe herdando `BaseModule`
3. Registre em `server.py`

### P: Como executar testes?

**R:**
```bash
# Todos os testes
python -m pytest tests/ -v

# Com coverage
python -m pytest tests/ --cov=.

# Teste específico
python -m pytest tests/test_filesystem.py::test_read_file -v
```

### P: Como contribuir com o projeto?

**R:** Este é um projeto pessoal, mas você pode:
- Fazer fork e adaptar para suas necessidades
- Sugerir melhorias
- Reportar bugs
- Compartilhar casos de uso interessantes

### P: Posso usar em produção comercial?

**R:** O projeto usa licença MIT, então sim, mas:
- Revise as dependências e suas licenças
- Adicione medidas de segurança adicionais
- Teste extensivamente
- Considere suporte profissional

### P: Como debugar problemas?

**R:**
```bash
# 1. Ativar debug
DEBUG=true python main.py

# 2. Ver logs detalhados
tail -f logs/mcp_server.log

# 3. Usar Python debugger
# Adicione no código:
import pdb; pdb.set_trace()

# 4. Testar isoladamente
python -c "from modules.filesystem.tools import FilesystemTools; import asyncio; asyncio.run(FilesystemTools().is_available())"
```

### P: Como atualizar dependências?

**R:**
```bash
# Ver versões atuais
pip list

# Atualizar tudo
pip install -r requirements.txt --upgrade

# Testar após atualizar
python test_server.py
python -m pytest tests/
```

---

## Perguntas Técnicas

### P: Por que usar FastMCP em vez de MCP direto?

**R:** FastMCP simplifica muito o desenvolvimento com decorators e registro automático de ferramentas.

### P: O servidor é assíncrono?

**R:** Sim! Usa `asyncio` para operações I/O não-bloqueantes.

### P: Qual o limite de tamanho de arquivo?

**R:** Padrão é 10MB (`MAX_FILE_SIZE` no `.env`). Você pode aumentar, mas considere a memória.

### P: Quantas operações simultâneas o servidor suporta?

**R:** Várias! Usa async para lidar com múltiplas requisições do Claude.

### P: Os dados são criptografados?

**R:** Não por padrão. Se necessário, use:
- Criptografia de disco do sistema operacional
- Criptografia específica para arquivos sensíveis

### P: Como fazer backup dos dados?

**R:**
```bash
# Backup manual
cp -r data/ backup/data_$(date +%Y%m%d)/

# Backup do banco de tarefas
cp data/tasks.json backup/tasks_$(date +%Y%m%d).json
```

### P: Posso usar com outros clientes MCP?

**R:** Sim! O servidor segue o protocolo MCP padrão. Qualquer cliente compatível pode usar.

### P: Como monitorar performance?

**R:**
- Logs mostram tempo de operações
- Use `htop`/`top` para recursos
- Ative DEBUG para métricas detalhadas

---

## Perguntas Avançadas

### P: Como integrar com minha API própria?

**R:** Crie um novo módulo em `modules/`:
```python
from modules.base import BaseModule
import httpx

class MinhaAPITools(BaseModule):
    async def is_available(self):
        return True
    
    async def initialize(self):
        self.client = httpx.AsyncClient()
        self.initialized = True
    
    def get_tools(self):
        return {
            "minha_funcao": self.minha_funcao
        }
    
    async def minha_funcao(self, param: str) -> str:
        response = await self.client.get(f"https://api.exemplo.com/{param}")
        return response.text
```

### P: Como limitar operações por tempo?

**R:** Já implementado! `OPERATION_TIMEOUT=30` no `.env`. Para mudar:
```env
OPERATION_TIMEOUT=60  # 60 segundos
```

### P: Como fazer deploy em servidor?

**R:** Não recomendado (é para uso local), mas se necessário:
1. Configure firewall
2. Adicione autenticação
3. Use HTTPS
4. Limite de rate
5. Monitoring e alertas

### P: Compatível com Docker?

**R:** Sim! Exemplo de Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## Ainda Tem Dúvidas?

1. 📖 Leia [COMO_USAR.md](COMO_USAR.md) para guia passo a passo
2. 📚 Consulte [GUIA_COMPLETO.md](GUIA_COMPLETO.md) para documentação detalhada
3. ⚡ Veja [QUICK_REFERENCE.md](QUICK_REFERENCE.md) para referência rápida
4. 📊 Verifique logs: `logs/mcp_server.log`
5. 🧪 Execute testes: `python test_server.py`

---

**💡 Dica:** A maioria dos problemas é resolvida reiniciando o Claude Desktop e o servidor!
