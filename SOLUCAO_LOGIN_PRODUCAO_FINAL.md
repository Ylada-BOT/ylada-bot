# 🔧 Solução: Login Funciona em Dev, Não em Produção

## 🔍 Problema Identificado

Em **desenvolvimento** funciona porque:
- ✅ Arquivo `data/users.json` existe localmente
- ✅ Sistema usa arquivo JSON quando banco não está disponível

Em **produção** não funciona porque:
- ❌ Arquivo `data/users.json` não existe (não é commitado no git)
- ❌ Sistema tenta usar banco de dados, mas usuário não existe lá
- ❌ Fallback para arquivo JSON falha porque arquivo não existe

---

## ✅ Soluções Implementadas

### 1. **Sincronização Automática JSON → Banco**

Quando um usuário faz login e é encontrado no arquivo JSON:
- ✅ Sistema automaticamente cria o usuário no banco de dados
- ✅ Próximos logins usarão o banco de dados
- ✅ Funciona em desenvolvimento e produção

### 2. **Criação Automática em Produção**

Se o usuário não existir em nenhum lugar e estiver em produção:
- ✅ Sistema tenta criar automaticamente no banco
- ✅ Usa email como nome padrão
- ✅ Role padrão: `user`

### 3. **Script SQL para Criar Usuário Manualmente**

Criei o script `scripts/criar_usuario_portalmagra.sql` para criar o usuário diretamente no banco.

---

## 🚀 Como Resolver AGORA

### **Opção 1: Executar Script SQL (Recomendado)** ⭐

1. Acesse o **Supabase SQL Editor**
2. Execute o script: `scripts/criar_usuario_portalmagra.sql`
3. Verifique se o usuário foi criado:
   ```sql
   SELECT * FROM users WHERE email = 'portalmagra@gmail.com';
   ```
4. Tente fazer login novamente

### **Opção 2: Usar Registro via Interface**

1. Acesse: https://yladabot.com/register
2. Preencha:
   - **Nome:** `PORTAL MAGRA`
   - **Email:** `portalmagra@gmail.com`
   - **Senha:** `123456`
3. Clique em "Cadastrar"
4. Faça login

### **Opção 3: Aguardar Sincronização Automática**

O sistema agora sincroniza automaticamente, mas você precisa:
1. Ter o arquivo `data/users.json` localmente
2. Fazer login uma vez em desenvolvimento
3. O sistema criará no banco automaticamente
4. Depois funcionará em produção

---

## 📋 Script SQL Completo

```sql
-- Execute no Supabase SQL Editor
INSERT INTO public.users (
    email,
    password_hash,
    name,
    role,
    is_active,
    created_at,
    updated_at
) VALUES (
    'portalmagra@gmail.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'PORTAL MAGRA',
    'user',
    true,
    NOW(),
    NOW()
)
ON CONFLICT (email) DO UPDATE
SET 
    password_hash = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    name = 'PORTAL MAGRA',
    is_active = true,
    updated_at = NOW();
```

---

## 🔍 Verificar se Funcionou

Após executar o script, verifique:

```sql
SELECT 
    id,
    email,
    name,
    role,
    is_active,
    created_at
FROM public.users
WHERE email = 'portalmagra@gmail.com';
```

Você deve ver:
- ✅ `email`: `portalmagra@gmail.com`
- ✅ `name`: `PORTAL MAGRA`
- ✅ `role`: `user`
- ✅ `is_active`: `true`

---

## 📝 Notas Importantes

1. **Hash da Senha**: O hash SHA256 de `123456` é: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`

2. **Em Produção**: O arquivo `data/users.json` não existe, então o sistema **sempre** usa o banco de dados.

3. **Sincronização**: O sistema agora sincroniza automaticamente usuários do JSON para o banco quando detecta que existe no JSON mas não no banco.

4. **Logs**: Verifique os logs do servidor em produção para ver exatamente o que está acontecendo:
   ```
   [DEBUG LOGIN] Tentando autenticar no banco de dados...
   [DEBUG LOGIN] Usuário não encontrado no banco, tentando modo simplificado...
   ```

---

## ✅ Próximos Passos

1. Execute o script SQL no Supabase
2. Tente fazer login em produção
3. Se ainda não funcionar, verifique os logs do servidor
4. Reporte o erro específico que aparece

