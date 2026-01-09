# 🔍 Diagnóstico: Login Não Funciona em Produção

## ⚠️ PROBLEMA

Login retorna erro **401 (Unauthorized)** - "Credenciais inválidas"

---

## 🔍 POSSÍVEIS CAUSAS

### **1. DATABASE_URL não atualizada no Railway** ⚠️ (Mais Provável)

A connection string no Railway ainda está com a senha antiga.

**Solução:**
1. Acesse Railway: https://railway.app
2. Selecione seu projeto
3. Clique no serviço **Flask/Python**
4. Vá em **Variables**
5. Encontre `DATABASE_URL`
6. Atualize com a nova connection string:
   ```
   postgresql://postgres.tbbjqvvtsotjqgfygaaj:whxOGnx1h098Ue2c@aws-0-us-west-2.pooler.supabase.com:5432/postgres
   ```
7. Salve e aguarde redeploy

---

### **2. Usuário não existe no banco de dados**

O usuário `portalmagra@gmail.com` pode não existir no banco de produção.

**Solução:**
1. Verifique se o usuário existe no Supabase:
   - Acesse Supabase → Table Editor → `users`
   - Procure por `portalmagra@gmail.com`

2. Se não existir, crie o usuário:
   - Via dashboard (registro)
   - Ou via SQL no Supabase

---

### **3. Senha incorreta**

A senha que você está usando não corresponde à senha no banco.

**Solução:**
1. Tente resetar a senha:
   - Clique em "Não tem conta? Cadastre-se"
   - Ou use a funcionalidade de "Esqueci minha senha"

2. Ou crie um novo usuário no banco

---

### **4. Banco de dados não está conectando**

O Railway pode não estar conseguindo conectar ao Supabase.

**Como verificar:**
1. No Railway, vá em **Deployments**
2. Veja os logs do último deploy
3. Procure por erros de conexão:
   - "Tenant or user not found"
   - "password authentication failed"
   - "connection failed"

---

## ✅ CHECKLIST DE VERIFICAÇÃO

- [ ] DATABASE_URL atualizada no Railway com nova senha
- [ ] Railway fez redeploy após atualizar DATABASE_URL
- [ ] Usuário existe no banco de dados (Supabase)
- [ ] Senha está correta
- [ ] Logs do Railway não mostram erros de conexão

---

## 🚀 SOLUÇÃO RÁPIDA

### **Passo 1: Atualizar DATABASE_URL no Railway**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. Clique no serviço **Flask/Python** (não o Node.js)
4. Vá em **Variables** (ou **Settings** → **Variables**)
5. Encontre `DATABASE_URL`
6. Clique em **Edit** ou **Update**
7. Cole esta connection string:
   ```
   postgresql://postgres.tbbjqvvtsotjqgfygaaj:whxOGnx1h098Ue2c@aws-0-us-west-2.pooler.supabase.com:5432/postgres
   ```
8. Clique em **Save**
9. Aguarde o redeploy automático (pode levar 1-2 minutos)

### **Passo 2: Verificar Logs**

1. No Railway, vá em **Deployments**
2. Clique no último deploy
3. Veja os logs
4. Procure por:
   - ✅ "Banco de dados conectado"
   - ✅ "Conexão bem-sucedida"
   - ❌ Erros de conexão

### **Passo 3: Verificar Usuário no Banco**

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá em **Table Editor** → `users`
4. Procure por `portalmagra@gmail.com`
5. Se não existir, crie via SQL ou dashboard

### **Passo 4: Testar Login Novamente**

1. Aguarde o redeploy completar
2. Tente fazer login novamente
3. Se ainda não funcionar, veja os logs do Railway

---

## 🔍 VERIFICAR LOGS DO RAILWAY

### **Como ver logs:**

1. No Railway, vá em **Deployments**
2. Clique no último deploy
3. Veja a aba **Logs**
4. Procure por erros relacionados a:
   - Banco de dados
   - Autenticação
   - Conexão

### **O que procurar:**

**✅ Bom:**
```
[✓] Banco de dados conectado
[✓] Carregado .env.local
Conexão bem-sucedida
```

**❌ Ruim:**
```
Tenant or user not found
password authentication failed
connection failed
Erro ao conectar ao banco
```

---

## 💡 DICA

Se o problema persistir:

1. **Verifique se o usuário existe:**
   - Acesse Supabase → Table Editor → `users`
   - Veja se `portalmagra@gmail.com` está lá

2. **Crie um novo usuário se necessário:**
   - Via dashboard: "Cadastre-se"
   - Ou via SQL no Supabase

3. **Verifique os logs do Railway:**
   - Eles vão mostrar exatamente qual é o problema

---

**Última atualização:** 27/01/2025

