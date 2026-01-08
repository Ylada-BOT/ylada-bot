# 👤 CRIAR USUÁRIO NO BANCO DE DADOS

**Data:** 2025-01-27  
**Situação:** Tabelas criadas, mas usuário não existe no banco

---

## 🎯 SOLUÇÃO: Criar Usuário no Banco

Agora que as tabelas foram criadas, você precisa criar o primeiro usuário no banco de dados.

---

## 🚀 MÉTODO 1: Via Interface (Recomendado)

### Passo 1: Acessar Registro

1. **Acesse:** https://yladabot.com/register
2. **Preencha o formulário:**
   - Nome: `PORTAL MAGRA`
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`
3. **Clique em "Cadastrar"**

### Passo 2: Verificar

Após cadastrar, o sistema deve:
- ✅ Salvar no banco de dados
- ✅ Redirecionar para login
- ✅ Permitir login normalmente

---

## 🔧 MÉTODO 2: Via SQL (Alternativa)

Se o registro via interface não funcionar, crie diretamente no banco:

### Passo 1: Acessar SQL Editor

1. **Acesse:** https://supabase.com
2. **SQL Editor** > **New query**

### Passo 2: Executar SQL

```sql
-- Criar usuário no banco de dados
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

**Nota:** O hash da senha `123456` é: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`

### Passo 3: Verificar

```sql
-- Verificar se usuário foi criado
SELECT id, email, name, role FROM users WHERE email = 'portalmagra@gmail.com';
```

---

## 🎯 POR QUE ISSO É NECESSÁRIO?

### Antes (Modo Simplificado):
- Usuários eram salvos em `data/users.json`
- Arquivo local, não persistia em produção

### Agora (Com Banco de Dados):
- Usuários são salvos no banco PostgreSQL
- Dados persistentes e seguros
- Mas precisa criar o primeiro usuário

---

## ✅ APÓS CRIAR USUÁRIO

1. **Faça login:**
   - Acesse: https://yladabot.com/login
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`

2. **Deve funcionar normalmente!**

---

## 🔍 VERIFICAÇÃO

### Teste via SQL:

```sql
-- Ver todos os usuários
SELECT * FROM users;
```

### Teste via API:

```bash
curl -X POST https://yladabot.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456"
  }'
```

**Resposta esperada:**
```json
{
  "success": true,
  "token": "...",
  "user": {
    "id": 1,
    "email": "portalmagra@gmail.com",
    "name": "PORTAL MAGRA",
    "role": "user"
  }
}
```

---

## 📋 CHECKLIST

- [x] ✅ Tabelas criadas
- [ ] ⏳ Usuário criado no banco
- [ ] ⏳ Login testado
- [ ] ⏳ Sistema funcionando

---

**Última atualização:** 2025-01-27

