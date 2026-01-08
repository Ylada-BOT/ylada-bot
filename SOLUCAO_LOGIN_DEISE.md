# ✅ Solução: Login Deise - Credenciais Inválidas

**Data:** 2025-01-27  
**Problema:** Login retorna 401 "Credenciais inválidas"  
**Status:** 🔧 **CORRIGIDO**

---

## ✅ O QUE FOI FEITO

### 1. Usuário Criado no Arquivo JSON ✅
- ✅ Email: `faulaandre@gmail.com`
- ✅ Senha: `Hbl@0842` (hash SHA256 correto)
- ✅ Nome: Deise
- ✅ Role: `admin`
- ✅ Arquivo: `data/users.json`

### 2. Logs de Debug Adicionados ✅
- ✅ Logs detalhados na autenticação
- ✅ Mostra qual modo está sendo usado
- ✅ Mostra se arquivo existe
- ✅ Mostra total de usuários

### 3. Teste Direto Funciona ✅
- ✅ Autenticação funciona quando testada diretamente
- ✅ Função retorna usuário corretamente

---

## 🚀 SOLUÇÃO: REINICIAR O SERVIDOR

O problema mais provável é que o servidor precisa ser **reiniciado** para carregar as mudanças.

### Passo 1: Parar o Servidor

Se o servidor estiver rodando:
- Pressione `Ctrl+C` no terminal onde está rodando
- Ou pare o processo

### Passo 2: Reiniciar o Servidor

```bash
cd "/Users/air/Ylada BOT"
python3 web/app.py
```

Ou se usar o script:

```bash
./start.sh
```

### Passo 3: Verificar Logs

Ao iniciar, você deve ver:
```
[!] Banco de dados não disponível: ...
[!] Sistema funcionará em modo simplificado (arquivo JSON)
[✓] Usuários carregados: 2 usuário(s)
```

### Passo 4: Tentar Login Novamente

1. Acesse: http://localhost:5002/login
2. Email: `faulaandre@gmail.com`
3. Senha: `Hbl@0842`
4. Clique em "Entrar"

**Deve funcionar agora!** ✅

---

## 🔍 SE AINDA NÃO FUNCIONAR

### Verificar Logs do Servidor

Após tentar fazer login, verifique os logs no console do servidor:

**Procure por:**
```
[DEBUG] Tentando autenticar: faulaandre@gmail.com
[DEBUG] Arquivo de usuários: /caminho/para/data/users.json
[DEBUG] Arquivo existe: True
[DEBUG] Total de usuários no arquivo: 2
[DEBUG] Email encontrado: faulaandre@gmail.com
[✓] Usuário autenticado: faulaandre@gmail.com
```

### Verificar Console do Navegador

No console do navegador (F12 > Console):
- Veja a resposta da API
- Verifique se há erros
- Veja o status code (deve ser 200, não 401)

### Teste Direto da API

Teste a API diretamente:

```bash
curl -X POST http://localhost:5002/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"faulaandre@gmail.com","password":"Hbl@0842"}'
```

**Resposta esperada:**
```json
{
  "success": true,
  "token": "eyJhbGci...",
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

- [x] Usuário criado no arquivo JSON
- [x] Hash da senha está correto
- [x] Teste direto funciona
- [x] Logs de debug adicionados
- [ ] **Servidor reiniciado** ⚠️ **IMPORTANTE**
- [ ] Login testado após reiniciar
- [ ] Logs verificados

---

## ⚠️ IMPORTANTE

**O servidor PRECISA ser reiniciado** para:
1. Carregar o novo usuário do arquivo JSON
2. Carregar as mudanças no código (logs de debug)
3. Garantir que está usando o modo simplificado

---

## 🎯 APÓS LOGIN FUNCIONAR

Quando o login funcionar:
1. ✅ Você será redirecionado para `/admin`
2. ✅ Terá acesso completo à área administrativa
3. ✅ Poderá gerenciar usuários, organizações, etc.

---

**Última atualização:** 2025-01-27

