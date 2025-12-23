# 🔐 Sistema de Autenticação - Configurado!

## ⚠️ Status Atual

**Autenticação está DESABILITADA por padrão** para facilitar o desenvolvimento.

Para ativar em produção, defina: `AUTH_REQUIRED=true`

## ✅ O que foi feito

O sistema de autenticação está **IMPLEMENTADO** e pode ser ativado quando necessário!

### Rotas Protegidas (requerem login):

**Páginas:**
- ✅ `/` - Dashboard principal
- ✅ `/flows` - Gerenciar fluxos
- ✅ `/flows/new` - Criar novo fluxo
- ✅ `/notifications` - Notificações
- ✅ `/leads` - Leads
- ✅ `/conversations` - Conversas
- ✅ `/qr` - QR Code do WhatsApp

**APIs:**
- ✅ `/api/ai/config` (POST) - Configurar IA
- ✅ `/api/conversations` - Listar conversas
- ✅ `/api/conversations/<chat_id>/messages` - Mensagens de conversa

### Rotas Públicas (não requerem login):

**Páginas:**
- ✅ `/login` - Página de login
- ✅ `/register` - Página de registro
- ✅ `/logout` - Logout

**APIs:**
- ✅ `/api/auth/*` - Rotas de autenticação (login, register)
- ✅ `/api/qr` - Obter QR Code (necessário para conectar)
- ✅ `/api/whatsapp-status` - Status do WhatsApp
- ✅ `/api/ai/config` (GET) - Ver configuração (sem API key)
- ✅ `/webhook` - Webhook para receber mensagens do WhatsApp

---

## 🚀 Como usar

### 1. Configurar Banco de Dados (se ainda não fez)

O sistema precisa de um banco de dados PostgreSQL para funcionar com autenticação.

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export DATABASE_URL="postgresql://usuario:senha@localhost/ylada_bot"
export SECRET_KEY="sua-chave-secreta-aqui"

# Criar banco de dados (se necessário)
createdb ylada_bot

# Inicializar banco (se houver script)
python scripts/init_db.py
```

### 2. Criar Primeiro Usuário

Você pode criar o primeiro usuário de duas formas:

**Opção A: Via API**
```bash
curl -X POST http://localhost:5002/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ylada.com",
    "password": "sua-senha-segura",
    "name": "Administrador"
  }'
```

**Opção B: Via Interface Web**
1. Acesse `http://localhost:5002/register`
2. Preencha o formulário
3. Faça login

### 3. Fazer Login

1. Acesse `http://localhost:5002/login`
2. Digite email e senha
3. Você será redirecionado para o dashboard

---

## 🔧 Configuração Avançada

### Desabilitar Autenticação (Apenas Desenvolvimento)

Se quiser desabilitar a autenticação temporariamente (apenas para desenvolvimento):

```bash
export AUTH_REQUIRED=false
python web/app.py
```

**⚠️ ATENÇÃO:** Nunca use isso em produção!

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Autenticação
AUTH_REQUIRED=true
SECRET_KEY=sua-chave-secreta-muito-longa-e-aleatoria-aqui

# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost/ylada_bot

# JWT (se usar tokens)
JWT_SECRET_KEY=sua-chave-jwt-aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

---

## 📋 Estrutura de Autenticação

### Sistema Implementado:

1. **Autenticação por Sessão** (Flask Session)
   - Usado para rotas de páginas
   - Armazena `user_id`, `user_email`, `user_role` na sessão

2. **Autenticação por Token JWT** (APIs)
   - Usado para rotas de API
   - Token no header `Authorization: Bearer <token>`
   - Decorator `@require_auth` disponível

3. **Roles de Usuário:**
   - `ADMIN` - Administrador
   - `RESELLER` - Revendedor
   - `USER` - Usuário final

### Decorators Disponíveis:

```python
# Para páginas (verifica sessão)
@require_login
def minha_rota():
    pass

# Para APIs (verifica sessão ou token)
@require_api_auth
def minha_api():
    pass

# Para APIs com token JWT (do blueprint auth)
from src.auth.authorization import require_auth
@require_auth
def minha_api():
    pass
```

---

## 🛡️ Segurança

### O que está protegido:

✅ Todas as páginas principais requerem login
✅ APIs sensíveis (configuração, conversas) requerem autenticação
✅ Senhas são hasheadas com bcrypt
✅ Tokens JWT com expiração
✅ Sessões seguras com SECRET_KEY

### Recomendações para Produção:

1. **Mude a SECRET_KEY:**
   ```python
   # Gere uma chave segura
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Use HTTPS:**
   - Configure SSL/TLS
   - Nunca envie tokens em HTTP

3. **Configure CORS adequadamente:**
   - Limite origens permitidas
   - Não use `CORS(app)` sem configuração

4. **Rate Limiting:**
   - Implemente rate limiting nas rotas de login
   - Proteja contra brute force

5. **Logs de Segurança:**
   - Monitore tentativas de login falhadas
   - Alerte sobre atividades suspeitas

---

## ❓ Problemas Comuns

### "Banco de dados não configurado"

**Solução:** Configure o PostgreSQL e crie o banco de dados.

### "Não consigo fazer login"

**Solução:** 
1. Verifique se criou um usuário primeiro (`/register`)
2. Verifique se o banco de dados está rodando
3. Verifique os logs do servidor

### "Quero desabilitar autenticação temporariamente"

**Solução:**
```bash
export AUTH_REQUIRED=false
python web/app.py
```

---

## 📝 Próximos Passos

1. ✅ Autenticação ativada
2. ⏳ Criar script de inicialização do banco
3. ⏳ Adicionar recuperação de senha
4. ⏳ Adicionar verificação de email
5. ⏳ Implementar rate limiting
6. ⏳ Adicionar logs de segurança

---

**Última atualização:** 13/12/2024

