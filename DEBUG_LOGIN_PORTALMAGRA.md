# 🔍 DEBUG: Login Portal Magra

## 📋 Informações do Usuário

- **Email:** `portalmagra@gmail.com`
- **Senha:** `123456`
- **Hash SHA256:** `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`
- **Status:** Existe no arquivo `data/users.json`

---

## 🔍 Diagnóstico

### 1. Verificar Logs do Servidor

Após tentar fazer login, verifique os logs do servidor. Você deve ver:

```
[DEBUG LOGIN] Tentando login para: portalmagra@gmail.com
[DEBUG LOGIN] DB_AVAILABLE: True/False
[DEBUG LOGIN] SIMPLE_AUTH_AVAILABLE: True/False
[DEBUG AUTH] Buscando usuário com email: portalmagra@gmail.com
[DEBUG AUTH] Total de usuários no arquivo: 2
[DEBUG AUTH] Verificando usuário ID 1: portalmagra@gmail.com
[DEBUG AUTH] Email encontrado! Verificando senha...
[DEBUG AUTH] Hash fornecido: 8d969eef6ecad3c29a3a...
[DEBUG AUTH] Hash armazenado: 8d969eef6ecad3c29a3a...
[✓] Usuário autenticado: portalmagra@gmail.com
```

### 2. Possíveis Problemas

#### Problema 1: Banco de Dados Tentando Primeiro
Se `DB_AVAILABLE: True`, o sistema tenta autenticar no banco primeiro. Se o usuário não existir no banco, deve fazer fallback para o arquivo JSON.

**Solução:** Verifique se o usuário existe no banco de dados Supabase.

#### Problema 2: Email com Espaços
O email pode ter espaços antes ou depois.

**Solução:** Use exatamente: `portalmagra@gmail.com` (sem espaços)

#### Problema 3: Senha Incorreta
A senha deve ser exatamente: `123456` (sem espaços)

---

## ✅ Soluções

### Solução 1: Verificar no Banco de Dados

Se o sistema está tentando usar o banco primeiro, verifique se o usuário existe:

```sql
SELECT id, email, name, role FROM users WHERE email = 'portalmagra@gmail.com';
```

Se não existir, crie:

```sql
INSERT INTO users (email, password_hash, name, role, is_active)
VALUES (
    'portalmagra@gmail.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'PORTAL MAGRA',
    'user',
    true
)
ON CONFLICT (email) DO NOTHING;
```

### Solução 2: Recadastrar

1. Acesse: https://yladabot.com/register
2. Preencha:
   - Nome: `PORTAL MAGRA`
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`
3. Clique em "Cadastrar"
4. Tente fazer login novamente

### Solução 3: Verificar Arquivo JSON em Produção

Se estiver em produção, o arquivo `data/users.json` pode não existir. Nesse caso, use o registro via interface ou API.

---

## 🚀 Teste Rápido

Tente fazer login com:
- **Email:** `portalmagra@gmail.com`
- **Senha:** `123456`

Se ainda não funcionar, verifique os logs do servidor para ver exatamente onde está falhando.

