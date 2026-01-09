# 🔧 Como Mudar para Session Pooler no Supabase

## 📍 ONDE FAZER A ALTERAÇÃO

### **PASSO 1: No Supabase (Interface Web)**

1. Na tela que você está vendo, procure o dropdown **"Method"**
2. Atualmente está em: **"Direct connection"**
3. **MUDE PARA:** **"Session Pooler"** (clique no dropdown e selecione)

### **PASSO 2: Copiar a Nova Connection String**

Depois de mudar para "Session Pooler", a connection string vai mudar automaticamente para algo assim:

```
postgresql://postgres.tbbjqvvtsotjqgfygaaj:[YOUR-PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

**Diferenças:**
- ✅ Agora usa `postgres.[PROJECT-REF]` (com ponto)
- ✅ Agora usa `pooler.supabase.com` (não `db.xxx.supabase.co`)
- ✅ Agora usa porta **6543** (não 5432)

### **PASSO 3: Copiar a Connection String**

1. Copie **TODA** a connection string que aparece na caixa de texto
2. **IMPORTANTE:** Substitua `[YOUR-PASSWORD]` pela senha real do seu banco

---

## 📝 ONDE COLAR (No Seu Computador)

### **PASSO 4: Abrir o Arquivo .env.local**

1. No seu computador, abra o projeto no editor (VS Code, Cursor, etc.)
2. Na raiz do projeto, abra o arquivo **`.env.local`**
3. Procure a linha que começa com `DATABASE_URL=`

### **PASSO 5: Substituir a Connection String**

1. **APAGUE** a linha antiga `DATABASE_URL=...`
2. **COLE** a nova connection string (do Passo 3)
3. **IMPORTANTE:** Certifique-se de substituir `[YOUR-PASSWORD]` pela senha real
4. Se a senha tiver caracteres especiais (`@`, `#`, etc.), codifique-os:
   - `@` → `%40`
   - `#` → `%23`
   - `%` → `%25`

**Exemplo final no .env.local:**
```bash
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:MinhaSenha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### **PASSO 6: Salvar e Testar**

1. **Salve** o arquivo `.env.local`
2. Teste a conexão:
```bash
python3 scripts/test_database_connection.py
```

---

## 🎯 RESUMO VISUAL

```
1. Supabase → Method: "Direct connection" 
   └─> MUDAR PARA: "Session Pooler"
   
2. Copiar connection string (com porta 6543)
   
3. Abrir .env.local no seu computador
   
4. Substituir DATABASE_URL=... pela nova string
   
5. Salvar e testar
```

---

## ⚠️ IMPORTANTE

- ✅ Use **Session Pooler** (porta 6543) - é mais compatível
- ✅ A connection string muda automaticamente quando você muda o Method
- ✅ Sempre substitua `[YOUR-PASSWORD]` pela senha real
- ✅ Codifique caracteres especiais na senha

---

**Última atualização:** 27/01/2025

