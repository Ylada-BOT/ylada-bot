# 🔧 SOLUÇÃO: Login em Produção

**Data:** 2025-01-27  
**Problema:** Erro "Credenciais inválidas" em produção  
**Causa:** Arquivo `users.json` não existe em produção

---

## 🐛 PROBLEMA

Em produção, o arquivo `data/users.json` não existe porque:
- Não está sendo commitado (dados locais)
- Cada ambiente precisa criar seus próprios usuários

---

## ✅ SOLUÇÕES

### Solução 1: Criar Usuário via API (Recomendado)

**Opção A: Usar endpoint `/api/auth/setup` (primeiro usuário)**

```bash
curl -X POST https://yladabot.com/api/auth/setup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456",
    "name": "PORTAL MAGRA"
  }'
```

**Opção B: Usar endpoint `/api/auth/register` (qualquer usuário)**

1. Acesse: https://yladabot.com/register
2. Preencha o formulário:
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`
   - Nome: `PORTAL MAGRA`
3. Clique em "Cadastrar"

### Solução 2: Criar Arquivo Manualmente (Via SSH/Console)

Se você tem acesso ao servidor:

```bash
# Criar diretório
mkdir -p data

# Criar arquivo users.json
cat > data/users.json << 'EOF'
{
  "1": {
    "id": 1,
    "email": "portalmagra@gmail.com",
    "password_hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
    "name": "PORTAL MAGRA",
    "role": "user",
    "is_active": true,
    "created_at": "2026-01-27T00:00:00"
  }
}
EOF
```

**Nota:** O hash da senha `123456` é: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`

---

## 🚀 PASSOS RECOMENDADOS

### Passo 1: Criar Primeiro Usuário

**Via Interface (Mais Fácil):**
1. Acesse: https://yladabot.com/register
2. Preencha:
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`
   - Nome: `PORTAL MAGRA`
3. Clique em "Cadastrar"

**Via API (Alternativa):**
```bash
curl -X POST https://yladabot.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456",
    "name": "PORTAL MAGRA"
  }'
```

### Passo 2: Fazer Login

1. Acesse: https://yladabot.com/login
2. Use as credenciais:
   - Email: `portalmagra@gmail.com`
   - Senha: `123456`
3. Clique em "Entrar"

---

## 🔍 VERIFICAÇÃO

### Teste se o usuário foi criado:

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
  "token": "eyJhbGci...",
  "user": {
    "id": 1,
    "email": "portalmagra@gmail.com",
    "name": "PORTAL MAGRA",
    "role": "user"
  }
}
```

---

## 📝 NOTA IMPORTANTE

### Por que isso acontece?

- O arquivo `data/users.json` é criado localmente
- Em produção, cada ambiente precisa criar seus próprios usuários
- Isso é normal e esperado para segurança

### Recomendação:

**Sempre crie o primeiro usuário via interface ou API após deploy!**

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Criar usuário em produção (via /register)
2. ✅ Fazer login
3. ✅ Conectar WhatsApp
4. ✅ Configurar IA
5. ✅ Criar fluxos

---

**Última atualização:** 2025-01-27

