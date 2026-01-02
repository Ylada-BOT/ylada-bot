# 🔑 Como Obter a Connection String do Supabase

## 📋 PASSO A PASSO

### **1. Acesse o Dashboard do Supabase**
- Vá para: https://supabase.com/dashboard/project/tbbjqvvtsotjqgfygaaj

### **2. Vá em Settings → Database**
- No menu lateral, clique em **Settings** (⚙️)
- Clique em **Database**

### **3. Encontre "Connection string"**
- Role a página até encontrar a seção **"Connection string"**
- Você verá várias abas: **URI**, **JDBC**, **Golang**, etc.

### **4. Selecione a aba "URI"**
- Clique na aba **"URI"**
- Você verá algo assim:
  ```
  postgresql://postgres.tbbjqvvtsotjqgfygaaj:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
  ```

### **5. Copie e Substitua a Senha**
- **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha do banco que você criou quando criou o projeto
- Se não lembrar da senha, você pode resetá-la:
  - Na mesma página, role até **"Database password"**
  - Clique em **"Reset database password"**
  - Anote a nova senha!

### **6. Cole no .env.local**
- Abra o arquivo `.env.local` na raiz do projeto
- Encontre a linha `DATABASE_URL=`
- Cole a connection string completa (com a senha substituída)

**Exemplo final:**
```bash
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:MinhaSenha123!@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

---

## ⚠️ IMPORTANTE

- **NUNCA** compartilhe a connection string com a senha
- **NUNCA** commite o arquivo `.env.local` no Git
- A senha do banco é **confidencial**

---

## 🧪 TESTAR CONEXÃO

Depois de configurar, teste:

```bash
# Reinicie o servidor Flask
python3 web/app.py
```

Se tudo estiver OK, você verá:
```
[✓] Banco de dados conectado
```

---

**Última atualização:** 23/12/2024




