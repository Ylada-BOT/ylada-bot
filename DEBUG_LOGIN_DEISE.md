# 🔍 DEBUG: Login Deise - Credenciais Inválidas

**Data:** 2025-01-27  
**Problema:** Login retorna 401 "Credenciais inválidas"  
**Status:** 🔍 Investigando

---

## ✅ VERIFICAÇÕES REALIZADAS

### 1. Usuário no Arquivo JSON ✅
- ✅ Usuário existe em `data/users.json`
- ✅ Email: `faulaandre@gmail.com`
- ✅ Hash da senha está correto
- ✅ Role: `admin`

### 2. Teste de Autenticação ✅
- ✅ Autenticação funciona quando testada diretamente
- ✅ Função `authenticate_user_simple()` retorna usuário corretamente

---

## 🐛 POSSÍVEIS CAUSAS

### 1. Servidor Não Reiniciado
- O servidor pode estar usando código antigo
- **Solução:** Reiniciar o servidor

### 2. Banco de Dados Tentando Primeiro
- Se `DB_AVAILABLE = True`, tenta banco primeiro
- Se não encontrar no banco, pode retornar erro antes de tentar JSON
- **Solução:** Verificar logs do servidor

### 3. Caminho do Arquivo Diferente
- Em produção, o caminho pode ser diferente
- **Solução:** Verificar caminho absoluto

---

## 🔧 CORREÇÕES APLICADAS

### 1. Logs de Debug Adicionados
- Logs ao tentar autenticar
- Logs do caminho do arquivo
- Logs se arquivo existe
- Logs do total de usuários
- Logs se email foi encontrado

### 2. Verificação Melhorada
- Verifica se arquivo existe antes de tentar ler
- Mostra total de usuários no arquivo
- Mensagens de erro mais detalhadas

---

## 🚀 PRÓXIMOS PASSOS

### 1. Reiniciar o Servidor

Se estiver rodando localmente:

```bash
# Parar servidor (Ctrl+C)
# Reiniciar
python3 web/app.py
# ou
./start.sh
```

### 2. Verificar Logs do Servidor

Após tentar fazer login, verifique os logs do console:

**Procure por:**
- `[DEBUG] Tentando autenticar: faulaandre@gmail.com`
- `[DEBUG] Arquivo de usuários: ...`
- `[DEBUG] Total de usuários no arquivo: 2`
- `[DEBUG] Email encontrado: ...`
- `[✓] Usuário autenticado: faulaandre@gmail.com`

### 3. Verificar Console do Navegador

No console do navegador (F12), verifique:
- Resposta da API `/api/auth/login`
- Mensagem de erro detalhada
- Status code (401, 500, etc)

### 4. Teste Direto da API

Teste a API diretamente:

```bash
curl -X POST http://localhost:5002/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"faulaandre@gmail.com","password":"Hbl@0842"}'
```

**Deve retornar:**
```json
{
  "success": true,
  "token": "...",
  "user": {
    "id": 2,
    "email": "faulaandre@gmail.com",
    "name": "Deise",
    "role": "admin"
  }
}
```

---

## 📋 CHECKLIST

- [ ] Servidor foi reiniciado após criar usuário
- [ ] Logs do servidor mostram tentativa de autenticação
- [ ] Arquivo `data/users.json` existe e tem 2 usuários
- [ ] Email está correto (sem espaços): `faulaandre@gmail.com`
- [ ] Senha está correta (sem espaços): `Hbl@0842`
- [ ] Teste direto da API funciona

---

## ⚠️ SE AINDA NÃO FUNCIONAR

### Verificar se DB_AVAILABLE está False

Adicione no início do arquivo `web/api/auth.py`:

```python
print(f"[DEBUG] DB_AVAILABLE: {DB_AVAILABLE}")
print(f"[DEBUG] SIMPLE_AUTH_AVAILABLE: {SIMPLE_AUTH_AVAILABLE}")
```

Isso vai mostrar qual modo está sendo usado.

### Forçar Modo Simplificado

Se o banco estiver causando problemas, você pode forçar o modo simplificado temporariamente comentando a verificação do banco.

---

**Última atualização:** 2025-01-27


