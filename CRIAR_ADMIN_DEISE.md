# 👤 Criar Usuário Administrador - Deise

**Email:** faulaandre@gmail.com  
**Nome:** Deise  
**Senha:** Hbl@0842  
**Role:** admin

---

## 🚀 Método Rápido (Recomendado)

### Passo 1: Acessar SQL Editor do Supabase

1. **Acesse:** https://supabase.com
2. **Faça login** no seu projeto
3. **No menu lateral**, clique em **"SQL Editor"** (ícone `</>`)
4. **Clique em "New query"**

### Passo 2: Executar SQL

1. **Abra o arquivo:** `scripts/create_admin_deise.sql`
2. **Copie TODO o conteúdo** do arquivo
3. **Cole no SQL Editor** do Supabase
4. **Clique em "Run"** (ou pressione Ctrl+Enter / Cmd+Enter)
5. **Aguarde alguns segundos**

### Passo 3: Verificar

O SQL já inclui uma query de verificação no final. Você deve ver:

```
id | email                    | name  | role  | is_active | created_at
---|--------------------------|-------|-------|-----------|------------
1  | faulaandre@gmail.com     | Deise | admin | true      | 2025-01-27...
```

---

## 📋 SQL Completo

Se preferir copiar diretamente:

```sql
-- Criar usuário administrador
INSERT INTO users (email, password_hash, name, role, is_active)
VALUES (
    'faulaandre@gmail.com',
    '$2b$12$DYSStWJ2bJsUaDJ/a4QJvug8XBDUwMxI/dx/mI/3ubNM8Zv9.cfC.',
    'Deise',
    'admin',
    true
)
ON CONFLICT (email) 
DO UPDATE SET
    password_hash = EXCLUDED.password_hash,
    name = EXCLUDED.name,
    role = EXCLUDED.role,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- Verificar se usuário foi criado
SELECT id, email, name, role, is_active, created_at 
FROM users 
WHERE email = 'faulaandre@gmail.com';
```

---

## ✅ Após Criar o Usuário

### 1. Fazer Login

1. **Acesse:** http://localhost:5002/login (ou sua URL de produção)
2. **Email:** `faulaandre@gmail.com`
3. **Senha:** `Hbl@0842`
4. **Clique em "Entrar"**

### 2. Acessar Área Administrativa

Após fazer login, você será redirecionado automaticamente para:
- **URL:** `/admin`
- **Dashboard administrativo** com todas as funcionalidades

---

## 🔒 Segurança

- ✅ Senha está com hash bcrypt (seguro)
- ✅ Role `admin` permite acesso completo
- ✅ Usuário está ativo (`is_active = true`)

---

## 🛠️ Script Python (Alternativa)

Se preferir usar o script Python:

```bash
cd "/Users/air/Ylada BOT"
python3 scripts/create_admin_user.py
```

O script vai gerar o SQL automaticamente.

---

## ⚠️ Importante

- Se o email já existir, o SQL vai **atualizar** o usuário (não vai dar erro)
- A senha será atualizada para `Hbl@0842`
- O role será atualizado para `admin`

---

**Última atualização:** 2025-01-27

