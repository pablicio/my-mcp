# 🚀 GUIA DE EXECUÇÃO - Correção de Dependências

## ⚡ Execução Rápida

Abra o PowerShell ou CMD na pasta do projeto e execute:

```bash
fix_dependencies.bat
```

---

## 📋 Passo a Passo Manual

Se preferir executar manualmente, siga estes passos:

### 1️⃣ Ativar Ambiente Virtual

```bash
venv\Scripts\activate.bat
```

Você deve ver `(venv)` no início da linha do terminal.

### 2️⃣ Desinstalar Pacotes Antigos

```bash
pip uninstall -y pydantic pydantic-settings
```

### 3️⃣ Atualizar pip

```bash
pip install --upgrade pip
```

### 4️⃣ Instalar Dependências Corrigidas

```bash
pip install -r requirements.txt
```

Você deve ver:
```
✅ Successfully installed pydantic-2.x.x
✅ Successfully installed pydantic-settings-2.x.x
✅ Successfully installed mcp-1.x.x
... (outras dependências)
```

### 5️⃣ Testar Importações

```bash
python test_imports.py
```

Resultado esperado:
```
✅ pydantic-settings importado com sucesso
✅ settings importado com sucesso
✅ MCPPersonalServer importado com sucesso
✅ FilesystemTools importado
✅ TasksTools importado
🎉 As correções funcionaram!
```

### 6️⃣ Teste Completo do Servidor

```bash
python test_server.py
```

Resultado esperado:
```
🧪 TESTE DO MCP SERVER PESSOAL
✅ Todas as importações OK
✅ Configurações verificadas
✅ Módulos carregados
✅ Servidor inicializado
🎉 Todos os testes passaram!
```

---

## 🐛 Resolução de Problemas

### Problema: "pip não é reconhecido"

```bash
# Use o caminho completo
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Problema: "Permissão negada"

Execute o CMD/PowerShell como Administrador

### Problema: "ModuleNotFoundError"

```bash
# Reinstale tudo
pip install --force-reinstall -r requirements.txt
```

### Problema: Versão do Python

```bash
# Verifique a versão (precisa ser 3.10+)
python --version

# Se for antiga, recrie o venv
python -m venv venv --clear
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## ✅ Checklist de Verificação

Após a execução, confirme:

- [ ] `pip list` mostra `pydantic-settings`
- [ ] `python test_imports.py` passa sem erros
- [ ] `python test_server.py` inicializa o servidor
- [ ] Não há mensagens de erro sobre `BaseSettings`
- [ ] Não há mensagens de erro sobre `Tool`

---

## 🎯 Próximos Passos (Após Sucesso)

1. **Inicie o servidor**:
   ```bash
   python main.py
   ```

2. **Configure o Claude Desktop**:
   - Edite `claude_desktop_config.json`
   - Adicione o servidor MCP
   - Reinicie o Claude Desktop

3. **Teste no Claude**:
   ```
   Liste arquivos no meu Documents
   ```

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs em `logs/mcp_server.log`
2. Execute `python test_imports.py` para diagnóstico
3. Compartilhe a mensagem de erro completa

---

**Última atualização**: 2025-10-18
**Status**: ✅ Pronto para executar
