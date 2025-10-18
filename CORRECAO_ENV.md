# 🔧 Correção do Erro ALLOWED_DIRECTORIES

## ❌ Problema

```
error parsing value for field "ALLOWED_DIRECTORIES" from source "DotEnvSettingsSource"
```

## 🎯 Causa

O `pydantic-settings` tem dificuldade com barras invertidas `\` do Windows em arquivos `.env`.

## ✅ Soluções

### Opção 1: Use barras normais (RECOMENDADO)
```env
ALLOWED_DIRECTORIES=C:/projetos
ALLOWED_DIRECTORIES=C:/Users/Usuario/Documents,C:/Users/Usuario/Desktop
```

### Opção 2: Use barras duplas
```env
ALLOWED_DIRECTORIES=C:\\projetos
ALLOWED_DIRECTORIES=C:\\Users\\Usuario\\Documents,C:\\Users\\Usuario\\Desktop
```

### Opção 3: Use aspas (se necessário)
```env
ALLOWED_DIRECTORIES="C:/projetos"
ALLOWED_DIRECTORIES="C:/Users/Usuario/Documents,C:/Users/Usuario/Desktop"
```

## 🔄 O que foi corrigido

### 1. Validador melhorado em `config/settings.py`
```python
@validator('ALLOWED_DIRECTORIES', pre=True)
def parse_directories(cls, v):
    """Parse directories from string or list."""
    if v is None:
        return []
    if isinstance(v, str):
        if not v.strip():
            return []
        # Remove aspas se existirem
        v = v.strip('"').strip("'")
        # Split por vírgula e limpa espaços
        dirs = [d.strip().strip('"').strip("'") for d in v.split(',') if d.strip()]
        return dirs
    if isinstance(v, list):
        return [str(d).strip() for d in v if d]
    return []
```

### 2. Arquivo `.env` atualizado
```env
# Antes (❌ causava erro)
ALLOWED_DIRECTORIES=C:\projetos

# Depois (✅ funciona)
ALLOWED_DIRECTORIES=C:/projetos
```

## 📝 Seu arquivo `.env` atual

O arquivo já foi corrigido para:
```env
ALLOWED_DIRECTORIES=C:/projetos
```

## 🧪 Teste agora

Execute:
```bash
python test_imports.py
```

Deve mostrar:
```
✅ settings importado com sucesso
📁 Diretórios: 1
```

## 📋 Exemplos de Configuração

### Um diretório
```env
ALLOWED_DIRECTORIES=C:/projetos
```

### Múltiplos diretórios
```env
ALLOWED_DIRECTORIES=C:/projetos,C:/Users/Usuario/Documents,C:/Users/Usuario/Desktop
```

### Com barras duplas
```env
ALLOWED_DIRECTORIES=C:\\projetos,C:\\Users\\Usuario\\Documents
```

### Diretório vazio (não recomendado)
```env
ALLOWED_DIRECTORIES=
```

## ⚠️ Dicas Importantes

1. **Sempre use `/` no Windows** - É mais seguro e compatível
2. **Separe por vírgula** - Não use ponto e vírgula
3. **Sem espaços extras** - Antes ou depois das vírgulas
4. **Caminhos absolutos** - Sempre use caminhos completos
5. **Verifique se existem** - Diretórios devem existir no disco

## ✅ Checklist

- [x] Validador corrigido em `config/settings.py`
- [x] Arquivo `.env` corrigido (barras normais)
- [x] Arquivo `.env.example` atualizado com exemplos
- [ ] **Teste executado com sucesso**

---

**Próximo passo**: Execute `python test_imports.py` para confirmar!
