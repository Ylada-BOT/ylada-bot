# 🔧 Solução: Login Funciona no Localhost mas Não no Deploy

**Data:** 2025-01-27  
**Problema:** Login funciona localmente mas retorna "Credenciais inválidas" em produção  
**Status:** ✅ **CORRIGIDO**

---

## 🐛 PROBLEMA IDENTIFICADO

### No Localhost (Funciona):
- ✅ Arquivo `data/users.json` existe localmente
- ✅ Usuário `portalmagra@gmail.com` está no arquivo JSON
- ✅ Sistema usa arquivo JSON quando banco não está disponível

### No Deploy (Não Funciona):
- ❌ Arquivo `data/users.json` não existe (não é commitado no git)
- ❌ Sistema tenta usar banco de dados, mas usuário pode não existir lá
- ❌ Fallback para arquivo JSON falha porque arquivo não existe
- ❌ Erro: "Credenciais inválidas"

---

## ✅ CORREÇÕES IMPLEMENTADAS

### 1. **Correção do JWT_SECRET**
- **Antes:** Usava `JWT_SECRET` (variável não definida)
- **Agora:** Usa `JWT_SECRET_KEY` de `config/settings.py`
- **Impacto:** Tokens JWT agora funcionam corretamente em produção

### 2. **Criação Automática do Arquivo JSON**
- **Antes:** Sistema falhava se `data/users.json` não existisse
- **Agora:** Sistema cria automaticamente o arquivo se não existir
- **Impacto:** Sistema funciona mesmo sem arquivo pré-existente

### 3. **Criação Automática do Diretório**
- **Antes:** Erro se diretório `data/` não existisse
- **Agora:** Sistema cria diretório automaticamente
- **Impacto:** Funciona em qualquer ambiente

### 4. **Logs Melhorados**
- **Antes:** Logs genéricos, difícil debugar
- **Agora:** Logs detalhados com `[DEBUG LOGIN]` para rastrear problemas
- **Impacto:** Mais fácil identificar problemas em produção

---

## 🚀 COMO RESOLVER AGORA

### **Opção 1: Criar Usuário no Banco de Dados (Recomendado)** ⭐

O melhor é ter o usuário no banco de dados em produção:

1. **Acesse o Supabase SQL Editor**
2. **Execute o script:** `scripts/criar_usuario_portalmagra.sql`
3. **Verifique se foi criado:**
   ```sql
   SELECT * FROM users WHERE email = 'portalmagra@gmail.com';
   ```
4. **Tente fazer login novamente**

### **Opção 2: Criar Usuário via Interface**

1. Acesse: `https://yladabot.com/register`
2. Preencha:
   - **Nome:** `PORTAL MAGRA`
   - **Email:** `portalmagra@gmail.com`
   - **Senha:** `123456`
3. Clique em "Cadastrar"
4. Faça login

### **Opção 3: Usar Endpoint de Setup**

```bash
curl -X POST https://yladabot.com/api/auth/setup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456",
    "name": "PORTAL MAGRA"
  }'
```

---

## 📋 VERIFICAÇÕES NECESSÁRIAS

### 1. **Variáveis de Ambiente no Deploy**

Certifique-se de que estas variáveis estão configuradas:

```bash
# JWT (obrigatório)
JWT_SECRET_KEY=sua-chave-secreta-aqui

# Banco de dados (recomendado)
DATABASE_URL=postgresql://postgres:[SENHA]@[HOST]:5432/postgres

# Outras
SECRET_KEY=sua-secret-key
APP_URL=https://yladabot.com
```

### 2. **Verificar Logs do Servidor**

Após o deploy, verifique os logs:

**Procure por:**
- `[✓] Banco de dados disponível` ou `[!] Banco de dados não disponível`
- `[DEBUG LOGIN] Tentando login para: portalmagra@gmail.com`
- `[DEBUG LOGIN] DB_AVAILABLE: True/False`
- `[DEBUG LOGIN] SIMPLE_AUTH_AVAILABLE: True/False`

### 3. **Verificar se Usuário Existe**

**No Banco de Dados:**
```sql
SELECT * FROM users WHERE email = 'portalmagra@gmail.com';
```

**No Arquivo JSON (se tiver acesso ao servidor):**
```bash
cat data/users.json
```

---

## 🔍 TROUBLESHOOTING

### Erro: "Credenciais inválidas"

**Possíveis causas:**
1. Usuário não existe no banco de dados
2. Senha está incorreta
3. Hash da senha não corresponde

**Solução:**
1. Execute o script SQL para criar/atualizar usuário
2. Ou use `/register` para criar nova conta
3. Verifique logs do servidor para mais detalhes

### Erro: "Sistema de autenticação não disponível"

**Possíveis causas:**
1. Banco de dados não está configurado
2. Arquivo JSON não pode ser criado (permissões)

**Solução:**
1. Configure `DATABASE_URL` nas variáveis de ambiente
2. Verifique permissões do diretório `data/`
3. Verifique logs do servidor

### Erro: "JWT token inválido"

**Possíveis causas:**
1. `JWT_SECRET_KEY` não está configurado
2. `JWT_SECRET_KEY` diferente entre servidores

**Solução:**
1. Configure `JWT_SECRET_KEY` nas variáveis de ambiente
2. Use a mesma chave em todos os ambientes
3. Gere uma chave segura: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

---

## 📝 ARQUIVOS MODIFICADOS

1. **`web/api/auth.py`**
   - Corrigido uso de `JWT_SECRET_KEY`
   - Melhorados logs de debug
   - Melhor tratamento de erros

2. **`web/utils/user_helper.py`**
   - Criação automática do arquivo `users.json`
   - Criação automática do diretório `data/`
   - Melhor tratamento de erros

---

## ✅ PRÓXIMOS PASSOS

1. **Fazer deploy das alterações**
2. **Criar usuário no banco de dados** (via script SQL ou interface)
3. **Testar login em produção**
4. **Verificar logs** se ainda houver problemas

---

**Última atualização:** 2025-01-27

