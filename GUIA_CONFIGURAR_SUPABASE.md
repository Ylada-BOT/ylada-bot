# 🚀 Guia: Configurar Supabase

## 📋 PASSO A PASSO

### **1. Criar Conta no Supabase**
1. Acesse: https://supabase.com
2. Clique em **"Start your project"** ou **"Sign up"**
3. Faça login com GitHub (recomendado) ou email

---

### **2. Criar Novo Projeto**
1. No dashboard, clique em **"New Project"**
2. Preencha:
   - **Name:** `ylada-bot` (ou outro nome)
   - **Database Password:** (anote essa senha!)
   - **Region:** Escolha a mais próxima (ex: South America)
3. Clique em **"Create new project"**
4. Aguarde ~2 minutos (criação do banco)

---

### **3. Obter Connection String**
1. No projeto criado, vá em **Settings** (⚙️) → **Database**
2. Role até **"Connection string"**
3. Selecione **"URI"**
4. Copie a string que aparece assim:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha que você criou

---

### **4. Configurar no Projeto**

#### **Opção A: Arquivo `.env.local` (Recomendado)**
Crie/edite o arquivo `.env.local` na raiz do projeto:

```bash
# Database
DATABASE_URL=postgresql://postgres:SUA_SENHA_AQUI@db.xxxxx.supabase.co:5432/postgres

# Ou separado (se preferir):
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=SUA_SENHA_AQUI
```

#### **Opção B: Variáveis de Ambiente**
```bash
export DATABASE_URL="postgresql://postgres:SUA_SENHA@db.xxxxx.supabase.co:5432/postgres"
```

---

### **5. Criar Tabelas no Supabase**
1. No Supabase, vá em **SQL Editor** (no menu lateral)
2. Clique em **"New query"**
3. Cole o conteúdo do arquivo `scripts/create_tables_supabase_fix.sql`
4. Clique em **"Run"** (ou `Cmd+Enter`)
5. Aguarde a execução (deve mostrar "Success")

---

### **6. Verificar Tabelas**
1. No Supabase, vá em **Table Editor**
2. Você deve ver as tabelas:
   - `users`
   - `plans`
   - `tenants`
   - `instances`
   - `flows`
   - `leads`
   - `conversations`
   - `messages`
   - `notifications`

---

### **7. Testar Conexão**
Reinicie o servidor Flask:
```bash
# Pare o servidor atual (Ctrl+C)
# E inicie novamente
python3 web/app.py
```

Se tudo estiver OK, você verá:
```
[✓] Banco de dados conectado
[✓] Rotas de organizations registradas
```

---

## 🔒 SEGURANÇA

### **⚠️ IMPORTANTE:**
- **NUNCA** commite o arquivo `.env.local` no Git
- Adicione `.env.local` ao `.gitignore`
- A senha do banco é **confidencial**

---

## 🐛 TROUBLESHOOTING

### **Erro: "Connection refused"**
- Verifique se a connection string está correta
- Confirme que substituiu `[YOUR-PASSWORD]` pela senha real
- Verifique se o projeto Supabase está ativo

### **Erro: "Table already exists"**
- Normal se já executou o script antes
- Pode ignorar ou usar `DROP TABLE IF EXISTS` antes

### **Erro: "Password authentication failed"**
- Verifique se a senha está correta
- Pode resetar a senha no Supabase: Settings → Database → Reset database password

---

## ✅ PRÓXIMOS PASSOS

Depois de configurar:
1. ✅ Testar criar uma organização
2. ✅ Testar criar um bot
3. ✅ Verificar se os dados aparecem no Supabase

---

**Última atualização:** 23/12/2024

