# 🔧 Correção de Dependências - MCP Tools 2

## Problemas Identificados

### 1. BaseSettings movido para pydantic-settings
**Erro**: `BaseSettings` has been moved to the `pydantic-settings` package

**Causa**: No Pydantic v2, `BaseSettings` foi separado em um pacote próprio

**Solução**: 
- ✅ Adicionado `pydantic-settings>=2.0.0` em `requirements.txt`
- ✅ Atualizado import em `config/settings.py`

### 2. Importação incorreta de Tool
**Erro**: cannot import name 'Tool' from 'mcp.server.models'

**Causa**: FastMCP não expõe `Tool` e `Resource` dessa forma

**Solução**:
- ✅ Removida importação desnecessária em `core/server.py`
- FastMCP usa decoradores, não precisa importar Tool diretamente

## Arquivos Modificados

### 1. requirements.txt
```diff
+ pydantic-settings>=2.0.0
```

### 2. config/settings.py
```diff
- from pydantic import BaseSettings, validator
+ from pydantic import validator, Field
+ from pydantic_settings import BaseSettings
```

### 3. core/server.py
```diff
- from mcp.server.models import Tool, Resource
```

## Como Aplicar as Correções

### Opção 1: Script Automático (Recomendado)
```bash
# Execute o script de correção
fix_dependencies.bat
```

### Opção 2: Manual
```bash
# 1. Ative o ambiente virtual
venv\Scripts\activate.bat

# 2. Desinstale pacotes antigos
pip uninstall -y pydantic pydantic-settings

# 3. Reinstale dependências
pip install -r requirements.txt

# 4. Teste o servidor
python test_server.py
```

## Verificação

Após aplicar as correções, você deve ver:

```
✅ Teste 1: Verificando importações...
   ✅ Todas as importações OK

✅ Teste 2: Verificando configurações...
   ...

✅ Todos os testes passaram! Servidor pronto para uso.
```

## Dependências Atualizadas

```
pydantic>=2.0.0,<3.0.0
pydantic-settings>=2.0.0  # ← NOVO
python-dotenv>=1.0.0
```

## Próximos Passos

1. ✅ Execute `fix_dependencies.bat`
2. ✅ Verifique que os testes passam
3. ✅ Execute `python main.py` para iniciar o servidor
4. ✅ Reinicie o Claude Desktop
5. ✅ Teste no Claude: "Liste arquivos no meu Documents"

## Notas Importantes

- **Pydantic v2**: O BaseSettings agora é um pacote separado
- **FastMCP**: Usa decoradores (@mcp.tool) ao invés de classes Tool
- **Compatibilidade**: Todas as alterações mantêm compatibilidade com o código existente

## Suporte

Se encontrar outros erros após as correções:

1. Verifique a versão do Python: `python --version` (requer 3.10+)
2. Limpe o cache: `pip cache purge`
3. Reinstale tudo: `pip install --force-reinstall -r requirements.txt`
4. Execute os testes: `python test_server.py`

---

**Data**: 2025-10-18
**Status**: ✅ Correções Aplicadas
