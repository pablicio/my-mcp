# 🏗️ Guia de Desenvolvimento

## Arquitetura do Projeto

### Estrutura de Diretórios

```
mcp-tools2/
├── config/              # Configurações centralizadas
│   ├── settings.py      # Settings com Pydantic
│   └── logging.py       # Configuração de logs
│
├── core/                # Núcleo do servidor MCP
│   ├── server.py        # Servidor principal
│   ├── registry.py      # Registro de ferramentas
│   └── security.py      # Validações de segurança
│
├── modules/             # Módulos funcionais (plugins)
│   ├── base.py          # Classe base para todos os módulos
│   ├── filesystem/      # Módulo de sistema de arquivos
│   ├── tasks/           # Módulo de tarefas
│   └── calendar/        # Módulo Google Calendar
│
├── utils/               # Utilitários compartilhados
│
└── tests/               # Testes centralizados
    ├── unit/            # Testes unitários
    ├── integration/     # Testes de integração
    └── quick_test.py    # Teste rápido de validação
```

## Criar um Novo Módulo

### 1. Estrutura Básica

Crie um novo diretório em `modules/`:

```
modules/
└── meu_modulo/
    ├── __init__.py
    ├── tools.py          # Ferramentas do módulo
    └── README.md         # Documentação do módulo
```

### 2. Implementar a Classe

```python
# modules/meu_modulo/tools.py
from modules.base import BaseModule
from typing import Dict, Callable, Any

class MeuModuloTools(BaseModule):
    """Descrição do seu módulo."""
    
    def __init__(self):
        super().__init__()
        # Inicialize atributos específicos aqui
        self.meu_recurso = None
    
    async def is_available(self) -> bool:
        """
        Verifica se o módulo está disponível.
        Retorne False se depende de recursos externos não disponíveis.
        """
        # Exemplo: verificar se uma API está acessível
        return True
    
    async def initialize(self):
        """
        Inicializa o módulo.
        Configure recursos, carregue configurações, etc.
        """
        try:
            # Inicialização aqui
            self.meu_recurso = "configurado"
            self.initialized = True
            self.logger.info("Módulo inicializado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro na inicialização: {e}")
            raise
    
    def get_tools(self) -> Dict[str, Callable]:
        """
        Retorna dicionário com as ferramentas disponíveis.
        Chave: nome da ferramenta
        Valor: função/método
        """
        return {
            "minha_ferramenta": self.minha_ferramenta,
            "outra_ferramenta": self.outra_ferramenta,
        }
    
    async def minha_ferramenta(self, param: str) -> str:
        """
        Descrição da ferramenta.
        Esta descrição será vista pelo Claude.
        
        Args:
            param: Descrição do parâmetro
            
        Returns:
            Descrição do retorno
        """
        try:
            self.logger.info(f"Executando minha_ferramenta com {param}")
            # Lógica da ferramenta aqui
            resultado = f"Processado: {param}"
            return resultado
        except Exception as e:
            self.logger.error(f"Erro em minha_ferramenta: {e}")
            return f"Erro: {e}"
    
    async def outra_ferramenta(self, **kwargs) -> Dict[str, Any]:
        """Outra ferramenta do módulo."""
        # Implementação
        return {"status": "ok"}
    
    async def cleanup(self):
        """
        Limpa recursos ao desligar o módulo.
        """
        await super().cleanup()
        # Limpeza específica do módulo
        self.meu_recurso = None
```

### 3. Registrar no Servidor

Edite `core/server.py`:

```python
from modules.meu_modulo.tools import MeuModuloTools

class MCPPersonalServer:
    # ...
    
    async def load_modules(self):
        """Carrega todos os módulos disponíveis."""
        modules_to_load = [
            ("calendar", CalendarTools),
            ("filesystem", FilesystemTools), 
            ("tasks", TasksTools),
            ("meu_modulo", MeuModuloTools),  # Adicione aqui
        ]
        # ... resto do código
```

### 4. Criar Testes

```python
# tests/unit/test_meu_modulo.py
import pytest
from modules.meu_modulo.tools import MeuModuloTools

@pytest.mark.asyncio
async def test_is_available():
    """Testa se o módulo está disponível."""
    module = MeuModuloTools()
    assert await module.is_available() == True

@pytest.mark.asyncio
async def test_initialize():
    """Testa inicialização do módulo."""
    module = MeuModuloTools()
    await module.initialize()
    assert module.initialized == True

@pytest.mark.asyncio
async def test_minha_ferramenta():
    """Testa a ferramenta principal."""
    module = MeuModuloTools()
    await module.initialize()
    
    resultado = await module.minha_ferramenta("teste")
    assert "Processado" in resultado
```

## Convenções de Código

### Nomenclatura

- **Classes**: PascalCase (`MinhaClasse`)
- **Funções/Métodos**: snake_case (`minha_funcao`)
- **Constantes**: UPPER_SNAKE_CASE (`MINHA_CONSTANTE`)
- **Privados**: Prefixo underscore (`_metodo_privado`)

### Documentação

Use docstrings para todas as funções públicas:

```python
async def minha_funcao(param1: str, param2: int = 0) -> Dict[str, Any]:
    """
    Breve descrição de uma linha.
    
    Descrição mais detalhada se necessário. Explique o que a função
    faz, não como ela faz.
    
    Args:
        param1: Descrição do primeiro parâmetro
        param2: Descrição do segundo parâmetro (opcional)
    
    Returns:
        Dicionário com os resultados contendo:
        - key1: Descrição
        - key2: Descrição
    
    Raises:
        ValueError: Quando param1 é inválido
        RuntimeError: Quando algo dá errado
    
    Example:
        >>> resultado = await minha_funcao("teste", 10)
        >>> print(resultado["key1"])
        valor
    """
    pass
```

### Logging

Use logging apropriadamente:

```python
self.logger.debug("Informação de debug detalhada")
self.logger.info("Operação normal importante")
self.logger.warning("Algo inesperado mas não crítico")
self.logger.error("Erro que precisa atenção")
self.logger.critical("Erro crítico do sistema")
```

### Tratamento de Erros

Sempre trate exceções adequadamente:

```python
async def operacao_com_erro(self):
    """Exemplo de tratamento de erros."""
    try:
        # Operação que pode falhar
        resultado = await operacao_perigosa()
        return resultado
    except ValueError as e:
        # Erro esperado e tratável
        self.logger.warning(f"Valor inválido: {e}")
        return {"error": str(e)}
    except Exception as e:
        # Erro inesperado
        self.logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise
```

## Testes

### Executar Testes

```bash
# Todos os testes
pytest tests/ -v

# Testes específicos
pytest tests/unit/test_meu_modulo.py -v

# Com coverage
pytest tests/ --cov=. --cov-report=html

# Teste rápido
python -m tests.quick_test
```

### Escrever Testes

- Um arquivo de teste por módulo
- Use fixtures para setup/teardown
- Teste casos normais e de erro
- Use mocks para dependências externas

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
async def meu_modulo():
    """Fixture que cria instância do módulo."""
    module = MeuModuloTools()
    await module.initialize()
    yield module
    await module.cleanup()

@pytest.mark.asyncio
async def test_com_fixture(meu_modulo):
    """Teste usando a fixture."""
    resultado = await meu_modulo.minha_ferramenta("teste")
    assert resultado is not None
```

## Segurança

### Validação de Entrada

Sempre valide entrada do usuário:

```python
from pathlib import Path
from core.security import SecurityValidator

async def operacao_com_arquivo(self, filepath: str) -> str:
    """Exemplo de validação segura."""
    # Validar caminho
    validator = SecurityValidator()
    if not validator.is_path_allowed(filepath):
        raise ValueError(f"Acesso negado: {filepath}")
    
    # Sanitizar entrada
    safe_path = Path(filepath).resolve()
    
    # Continuar operação...
```

### Limites

Implemente limites razoáveis:

```python
MAX_RESULTS = 1000
TIMEOUT_SECONDS = 30

async def operacao_com_limite(self):
    """Exemplo com timeout."""
    try:
        resultado = await asyncio.wait_for(
            operacao_demorada(),
            timeout=TIMEOUT_SECONDS
        )
        return resultado
    except asyncio.TimeoutError:
        self.logger.error("Operação excedeu timeout")
        raise
```

## Performance

### Operações Assíncronas

Use async/await para operações I/O:

```python
import aiofiles
import asyncio

async def ler_multiplos_arquivos(self, arquivos: List[str]):
    """Lê múltiplos arquivos em paralelo."""
    async def ler_arquivo(filepath):
        async with aiofiles.open(filepath, 'r') as f:
            return await f.read()
    
    # Executa em paralelo
    resultados = await asyncio.gather(
        *[ler_arquivo(f) for f in arquivos]
    )
    return resultados
```

### Cache

Use cache quando apropriado:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def operacao_cara(param: str) -> str:
    """Cacheia resultados de operações custosas."""
    # Operação cara aqui
    return resultado
```

## Debugging

### Modo Debug

Ative debug no `.env`:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

### Python Debugger

Use pdb para debugging:

```python
import pdb

async def funcao_com_bug(self):
    # ... código ...
    pdb.set_trace()  # Breakpoint aqui
    # ... mais código ...
```

### Logs Úteis

Adicione logs úteis para debugging:

```python
self.logger.debug(f"Estado atual: {self.estado}")
self.logger.debug(f"Parâmetros recebidos: {locals()}")
```

## Versionamento

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Documente mudanças importantes
- Mantenha compatibilidade quando possível

## Recursos Úteis

- [MCP Documentation](https://modelcontextprotocol.io)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Pytest Documentation](https://docs.pytest.org)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)
