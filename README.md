# 🚀 MCP Server Pessoal v1.0.0

<div align="center">

**Servidor extensível baseado no Model Context Protocol (MCP)**  
**Permite ao Claude Desktop acessar seus recursos locais de forma segura**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-1.2.0-green.svg)](https://modelcontextprotocol.io)

[Instalação](#-instalação-rápida) • [Configuração](#️-configuração) • [Uso](#-exemplos-de-uso) • [Testes](#-testes) • [Documentação](#-documentação)

</div>

---

## ✨ Características

### 🔒 Segurança em Primeiro Lugar
- ✅ Validação rigorosa de caminhos (proteção contra path traversal)
- ✅ Lista de diretórios permitidos (allowlist)
- ✅ Sanitização de nomes de arquivos
- ✅ Limite de tamanho de arquivos (10MB)
- ✅ Timeout de operações (30s)
- ✅ Logging completo de todas as ações

### 📁 Gerenciamento de Arquivos
- Leitura e escrita de arquivos
- Listagem de diretórios (recursiva opcional)
- Busca de arquivos por padrão
- Informações detalhadas de arquivos
- Criação e deleção segura

### ✅ Sistema de Tarefas
- Criar, listar e gerenciar tarefas
- Prioridades (alta, média, baixa)
- Status de conclusão
- Datas de prazo
- Sistema de notas com tags

### 📅 Google Calendar (Opcional)
- Criar eventos
- Listar compromissos
- Buscar eventos
- Integração OAuth2

### 🛠️ Arquitetura Extensível
- Sistema modular baseado em plugins
- Fácil adição de novos módulos
- Registro automático de ferramentas
- Testes unitários incluídos

---

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.9 ou superior
- Claude Desktop instalado
- Windows, macOS ou Linux

### Setup Automatizado (Recomendado)

```bash
# 1. Navegue até o diretório do projeto
cd C:\projetos\IA\mcp\mcp-tools2

# 2. Execute o setup
python setup.py

# 3. Siga as instruções na tela
```

O script irá:
- ✅ Verificar Python 3.9+
- ✅ Instalar todas as dependências
- ✅ Criar arquivo .env com suas configurações
- ✅ Configurar o Claude Desktop automaticamente
- ✅ Criar estrutura de diretórios necessária
- ✅ Executar testes de validação

---

## ⚙️ Configuração

### 1. Arquivo .env

Edite `.env` e configure seus diretórios permitidos:

```env
# USE CAMINHOS ABSOLUTOS!
# Windows
ALLOWED_DIRECTORIES=C:\\Users\\SeuUsuario\\Documents,C:\\Users\\SeuUsuario\\Desktop

# Linux/Mac
ALLOWED_DIRECTORIES=/home/usuario/Documents,/home/usuario/Desktop

# Servidor
DEBUG=false
LOG_LEVEL=INFO
```

**⚠️ IMPORTANTE:** Use sempre caminhos absolutos!

---

## 🎮 Uso

### Iniciar o Servidor

```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Ou diretamente
python main.py
```

### Usar no Claude Desktop

1. **Reinicie o Claude Desktop** (importante!)
2. Abra uma nova conversa
3. Digite seus comandos

---

## 💡 Exemplos de Uso

### 📁 Arquivos

```
Liste os arquivos na minha pasta Documents
Leia o arquivo README.md
Crie arquivo teste.py com Hello World
Procure arquivos .txt em Documents
```

### ✅ Tarefas

```
Crie tarefa: "Revisar docs" prioridade alta
Mostre minhas tarefas pendentes
Marque tarefa #3 como concluída
```

### 📅 Calendar

```
Crie evento "Reunião" amanhã às 14h
Quais meus compromissos hoje?
```

---

## 🧪 Testes

```bash
# Teste rápido
python test_server.py

# Testes unitários
python -m pytest tests/ -v
```

**📚 Documentação completa:** [TESTES.md](TESTES.md)

---

## 🐛 Troubleshooting

### Claude não encontra o servidor

1. Reinicie o Claude Desktop completamente
2. Verifique `claude_desktop_config.json`
3. Teste: `python main.py`
4. Verifique logs: `logs/mcp_server.log`

### Erro "Diretório não permitido"

1. Verifique `ALLOWED_DIRECTORIES` em `.env`
2. Use caminhos absolutos
3. Verifique que o diretório existe

### Erro de importação

```bash
pip install -r requirements.txt --force-reinstall
```

**📚 Troubleshooting completo:** [GUIA_COMPLETO.md](GUIA_COMPLETO.md)

---

## 📊 Estrutura do Projeto

```
mcp-tools2/
├── main.py              # Entrada do servidor
├── setup.py             # Setup automatizado
├── test_server.py       # Teste rápido
│
├── config/              # Configurações
├── core/                # Núcleo do servidor
├── modules/             # Módulos funcionais
│   ├── filesystem/      # Sistema de arquivos
│   ├── tasks/           # Tarefas e notas
│   └── calendar/        # Google Calendar
│
├── tests/               # Testes unitários
├── logs/                # Arquivos de log
└── data/                # Dados (tarefas, etc)
```

---

## 📚 Documentação

- **[README.md](README.md)** - Visão geral (este arquivo)
- **[GUIA_COMPLETO.md](GUIA_COMPLETO.md)** - Guia detalhado
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Referência rápida
- **[TESTES.md](TESTES.md)** - Guia de testes

---

## 🛠️ Desenvolvimento

### Adicionar Novo Módulo

1. Crie diretório em `modules/`
2. Implemente classe herdando `BaseModule`
3. Registre no `server.py`

```python
# modules/meu_modulo/tools.py
from modules.base import BaseModule

class MeuModuloTools(BaseModule):
    async def is_available(self) -> bool:
        return True
    
    async def initialize(self):
        self.initialized = True
    
    def get_tools(self):
        return {
            "minha_ferramenta": self.minha_ferramenta
        }
    
    async def minha_ferramenta(self, param: str) -> str:
        """Descrição da ferramenta."""
        return f"Resultado: {param}"
```

---

## 🔒 Segurança

- ✅ Validação de paths (sem `../`)
- ✅ Allowlist de diretórios
- ✅ Limite de tamanho de arquivo
- ✅ Timeout de operações
- ✅ Logging de todas operações
- ✅ Sanitização de nomes

---

## 📈 Roadmap

- [ ] Interface web para configuração
- [ ] Integração com mais APIs (Gmail, Notion)
- [ ] Sistema de plugins
- [ ] Sincronização multi-dispositivo
- [ ] Backup automático

---

## 🤝 Contribuição

Este é um projeto pessoal desenvolvido para uso com Claude Desktop.  
Sugestões e feedback são bem-vindos!

---

## 📝 Licença

MIT License - Use como desejar!

---

## 🆘 Suporte

- 📖 Documentação: Veja os arquivos `.md`
- 📊 Logs: `./logs/mcp_server.log`
- 🐛 Debug: `DEBUG=true python main.py`

---

<div align="center">

**Desenvolvido com ❤️ usando Model Context Protocol**

[🏠 Home](#-mcp-server-pessoal-v100) • [📖 Docs](GUIA_COMPLETO.md) • [⚡ Quick Ref](QUICK_REFERENCE.md) • [🧪 Tests](TESTES.md)

</div>
