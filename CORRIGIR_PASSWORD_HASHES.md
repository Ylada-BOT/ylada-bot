# 🔧 Corrigir Password Hashes no Banco

## ⚠️ PROBLEMA

Os `password_hash` no banco podem estar em formato incorreto:
- ❌ SHA256 (não funciona com o sistema)
- ❌ Hash muito curto
- ❌ Formato incompatível

O sistema usa **bcrypt**, que tem formato específico:
- ✅ Começa com `$2b$` ou `$2a$`
- ✅ Tem 60 caracteres
- ✅ Exemplo: `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5`

---

## ✅ SOLUÇÃO

### **Opção 1: Resetar Senha via Dashboard (Mais Fácil)**

1. Acesse: `https://yladabot.com/register`
2. Tente criar uma nova conta (se não existir)
3. Ou use funcionalidade "Esqueci minha senha" (se existir)
4. Isso vai gerar o hash bcrypt correto automaticamente

### **Opção 2: Criar Script SQL para Resetar Senhas**

Crie um script que gera hashes bcrypt corretos. Mas isso é complexo porque precisa gerar o hash no Python.

### **Opção 3: Usar Python para Gerar Hash Correto**

Execute este script localmente para gerar o hash bcrypt:

```python
import bcrypt

# Senha que você quer usar
senha = "123456"  # ou outra senha

# Gera hash bcrypt
hash_bcrypt = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"Hash bcrypt: {hash_bcrypt}")
```

Depois use esse hash no SQL.

---

## 🔍 VERIFICAR FORMATO DOS HASHES

### **Hash Bcrypt (Correto):**
- Começa com: `$2b$` ou `$2a$`
- Tamanho: 60 caracteres
- Exemplo: `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5`

### **Hash SHA256 (Incorreto):**
- Tamanho: 64 caracteres
- Exemplo: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`
- ❌ Não funciona com o sistema!

---

## 🚀 SOLUÇÃO RÁPIDA

### **Para o usuário portalmagra@gmail.com:**

1. **Gere hash bcrypt da senha desejada:**
   ```bash
   python3 -c "import bcrypt; print(bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8'))"
   ```

2. **Copie o hash gerado**

3. **No Supabase, execute este SQL:**
   ```sql
   UPDATE public.users
   SET password_hash = 'HASH_GERADO_AQUI'
   WHERE email = 'portalmagra@gmail.com';
   ```

4. **Ou use o Table Editor:**
   - Clique no usuário `portalmagra@gmail.com`
   - Edite o campo `password_hash`
   - Cole o hash bcrypt gerado
   - Salve

---

## 📋 CHECKLIST

- [ ] Verificar formato dos password_hash no banco
- [ ] Identificar quais estão em SHA256 (incorretos)
- [ ] Gerar hash bcrypt correto para cada usuário
- [ ] Atualizar no banco
- [ ] Testar login

---

**Última atualização:** 27/01/2025

