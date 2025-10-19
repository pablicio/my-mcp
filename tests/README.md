# 🧪 MCP Server - Suite de Testes

Testes organizados e abrangentes para o MCP Personal Server.

## 📁 Estrutura

```
tests/
├── unit/               # Testes unitários de componentes individuais
├── integration/        # Testes de integração da API REST
├── mcp/               # Testes de protocolo MCP e conexão com Claude
└── run_tests.py       # Script de execução de testes
```

## 🚀 Executando Testes

### Todos os testes
```bash
python tests/run_tests.py
```

### Testes específicos

**Testes Unitários:**
```bash
pytest tests/unit/ -v
```

**Testes de Integração (API):**
```bash
# Certifique-se que o servidor está rodando!
python api_server.py

# Em outro terminal:
pytest tests/integration/ -v
```

**Testes MCP/Claude:**
```bash
pytest tests/mcp/ -v
```

## 📋 Testes Disponíveis

### Unit Tests
- Testes de módulos individuais
- Validação de funções isoladas
- Mocks e fixtures

### Integration Tests
- **test_api_endpoints.py** - Teste rápido de endpoints
- **test_api_complete.py** - Suite completa com todos os endpoints

### MCP Tests
- **test_claude_connection.py** - Testes de conexão e comunicação MCP
  - Inicialização do servidor
  - Registro de ferramentas
  - Criação e manipulação de tarefas via MCP
  - Persistência de dados
  - Tratamento de erros
  - Operações concorrentes

## 🔧 Dependências

```bash
pip install pytest pytest-asyncio colorama requests
```

## ✅ Boas Práticas

1. **Isolamento**: Cada teste é independente
2. **Fixtures**: Uso de fixtures para setup/teardown
3. **Async Support**: Suporte completo a operações assíncronas
4. **Coverage**: Cobertura de casos de sucesso e erro
5. **Documentação**: Todos os testes documentados

## 📊 Cobertura

Execute com coverage:
```bash
pytest --cov=. --cov-report=html tests/
```

## 🐛 Debugging

Para debug detalhado:
```bash
pytest -vv --tb=long --log-cli-level=DEBUG tests/
```

## 📝 Adicionando Novos Testes

### Teste Unitário
```python
# tests/unit/test_my_module.py
import pytest

def test_my_function():
    result = my_function()
    assert result == expected
```

### Teste de Integração
```python
# tests/integration/test_my_api.py
import requests

def test_api_endpoint():
    response = requests.get('http://localhost:5000/api/endpoint')
    assert response.status_code == 200
```

### Teste MCP
```python
# tests/mcp/test_my_tool.py
import pytest

@pytest.mark.asyncio
async def test_mcp_tool(server):
    result = await server.modules['tasks'].my_tool()
    assert 'success' in result
```

## 🎯 Objetivos de Cobertura

- [ ] 80%+ de cobertura de código
- [x] Todos os endpoints API testados
- [x] Protocolo MCP validado
- [x] Testes de conexão com Claude
- [ ] Testes de performance
- [ ] Testes de carga

## 📞 Suporte

Para problemas com testes, verifique:
1. Servidor está rodando (para testes de integração)
2. Dependências instaladas
3. Banco de dados de teste limpo
4. Portas disponíveis
