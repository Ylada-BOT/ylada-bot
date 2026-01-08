# 🔍 DEBUG: Login em Produção - Credenciais Inválidas

**Data:** 2025-01-27  
**Problema:** Cadastro funciona, mas login retorna "credenciais inválidas"  
**Status:** 🔍 Investigando

---

## 🐛 PROBLEMA

- ✅ Cadastro funciona (redireciona)
- ❌ Login retorna "credenciais inválidas" (401)

---

## 🔍 POSSÍVEIS CAUSAS

### 1. Arquivo Não Está Sendo Salvo
- O arquivo `data/users.json` pode não estar sendo criado em produção
- Permissões de escrita podem estar faltando
- Diretório `data/` pode não existir

### 2. Arquivo Está Sendo Salvo em Local Diferente
- Em produção, o caminho pode ser diferente
- Arquivo pode estar sendo salvo mas não lido do mesmo lugar

### 3. Problema de Permissões
- Servidor pode não ter permissão para escrever no diretório
- Arquivo pode estar sendo criado mas não lido

---

## ✅ CORREÇÕES APLICADAS

### 1. Logs Detalhados
- Logs ao salvar usuários
- Logs ao carregar usuários
- Verificação se usuário foi salvo corretamente

### 2. Verificação de Salvamento
- Após salvar, verifica se foi salvo corretamente
- Mostra hash da senha (parcial) para debug

### 3. Tratamento de Erros Melhorado
- Mensagens de erro mais claras
- Traceback completo em caso de erro

---

## 🚀 PRÓXIMOS PASSOS

### 1. Verificar Logs do Servidor

Após o deploy, verifique os logs do servidor em produção:

```bash
# Se tiver acesso SSH
tail -f /var/log/app.log
# ou
journalctl -u app -f
```

**Procure por:**
- `[✓] Usuário criado e verificado`
- `[✓] Usuários salvos em`
- `[✓] Usuários carregados`
- `[!] Arquivo de usuários não encontrado`

### 2. Verificar Arquivo Diretamente

Se tiver acesso ao servidor:

```bash
# Verificar se arquivo existe
ls -la data/users.json

# Ver conteúdo
cat data/users.json

# Verificar permissões
stat data/users.json
```

### 3. Teste via API

```bash
# Teste de registro
curl -X POST https://yladabot.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456",
    "name": "PORTAL MAGRA"
  }'

# Teste de login (logo após)
curl -X POST https://yladabot.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456"
  }'
```

---

## 💡 SOLUÇÃO TEMPORÁRIA

### Se o Problema Persistir:

**Opção 1: Usar Endpoint /setup**

```bash
curl -X POST https://yladabot.com/api/auth/setup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456",
    "name": "PORTAL MAGRA"
  }'
```

Este endpoint cria o primeiro usuário e garante que funcione.

**Opção 2: Verificar Variáveis de Ambiente**

Em produção, verifique se o diretório `data/` está acessível:

```bash
# Verificar se diretório existe
ls -la data/

# Criar se não existir
mkdir -p data
chmod 755 data
```

---

## 📋 CHECKLIST DE DEBUG

- [ ] Verificar logs do servidor após cadastro
- [ ] Verificar se arquivo `data/users.json` existe
- [ ] Verificar permissões do arquivo
- [ ] Verificar conteúdo do arquivo
- [ ] Testar login via API
- [ ] Verificar se email está em lowercase
- [ ] Verificar se senha está correta

---

## 🎯 RESULTADO ESPERADO

Após as correções, os logs devem mostrar:

```
[✓] Usuário criado: PORTAL MAGRA (portalmagra@gmail.com) - ID: 1
[✓] Usuários salvos em /path/to/data/users.json
[✓] Total de usuários: 1
[✓] Usuário criado e verificado: PORTAL MAGRA (portalmagra@gmail.com) - ID: 1
[✓] Hash da senha: 8d969eef6ecad3c29a3a...
```

E no login:

```
[✓] Usuários carregados: 1 usuário(s)
[✓] Usuário autenticado: portalmagra@gmail.com
```

---

**Última atualização:** 2025-01-27  
**Status:** 🔍 **AGUARDANDO LOGS PARA DEBUG**

