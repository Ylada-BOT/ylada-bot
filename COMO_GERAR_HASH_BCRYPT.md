# 🔑 Como Gerar Hash Bcrypt

## ⚠️ IMPORTANTE

**NÃO execute comandos Python no SQL Editor do Supabase!**

O SQL Editor só executa SQL, não Python.

---

## ✅ FORMA CORRETA

### **Passo 1: Gerar Hash no Terminal Local**

No seu computador, execute:

```bash
python3 -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8'))"
```

**Ou se estiver no ambiente virtual:**

```bash
source venv/bin/activate
python3 -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8'))"
```

**Resultado:** Você verá algo como:
```
$2b$12$XDMAsFTlDzxuzJm/P9nkBu9K9MS8UBp6yfr5NAjzvuRqdAJtsjiMS
```

### **Passo 2: Copiar o Hash**

Copie o hash completo (começa com `$2b$` e tem 60 caracteres).

### **Passo 3: Usar no SQL Editor**

No Supabase SQL Editor, execute:

```sql
UPDATE public.users
SET 
    password_hash = '$2b$12$XDMAsFTlDzxuzJm/P9nkBu9K9MS8UBp6yfr5NAjzvuRqdAJtsjiMS',
    updated_at = NOW()
WHERE email = 'portalmagra@gmail.com';
```

**Substitua o hash pelo que você gerou!**

---

## 🚀 SOLUÇÃO RÁPIDA

Já gerei um hash para você! Use este script SQL:

**Arquivo:** `scripts/atualizar_senha_portalmagra_agora.sql`

1. Abra o arquivo no seu editor
2. Copie todo o conteúdo
3. Cole no Supabase SQL Editor
4. Clique em **Run**
5. Pronto! ✅

---

## 📋 RESUMO

| Onde | O que fazer |
|------|-------------|
| **Terminal local** | Gerar hash bcrypt com Python |
| **SQL Editor** | Executar SQL UPDATE com o hash |

**NÃO misture!** Python no terminal, SQL no editor.

---

**Última atualização:** 27/01/2025

