# 🚀 Atualizar Vercel para Multi-Instance (4 Telefones)

## ✅ Situação Atual:
- Você já está fazendo deploy na Vercel
- Está usando `web/app.py` (versão antiga)
- Precisa atualizar para `web/app_multi.py` (multi-instance)

---

## 🔧 Passo 1: Atualizar Entry Point

### Opção A: Substituir (Recomendado)

Edite `api/index.py`:

```python
"""
Vercel Serverless Function Entry Point - Multi-Instance
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'src'))

# Mude de app.py para app_multi.py
from web.app_multi import app
```

### Opção B: Manter Ambos (Temporário)

Crie `api/index_multi.py` e atualize `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index_multi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index_multi.py"
    }
  ]
}
```

---

## 🗄️ Passo 2: Configurar Banco de Dados (Supabase)

### 2.1 Criar Tabelas no Supabase

Acesse seu projeto Supabase e execute este SQL:

```sql
-- Tabela de Contas
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'owner',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de Instâncias
CREATE TABLE IF NOT EXISTS instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    instance_name VARCHAR(100) NOT NULL,
    port INTEGER UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'disconnected',
    qr_code TEXT,
    last_connected TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, instance_name)
);

-- Tabela de Contatos
CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, phone)
);

-- Tabela de Conversas
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id),
    message TEXT NOT NULL,
    from_me BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Tabela de Campanhas
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    message TEXT,
    qr_code_url TEXT,
    link TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_contacts_account ON contacts(account_id);
CREATE INDEX IF NOT EXISTS idx_conversations_account ON conversations(account_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_account ON campaigns(account_id);
CREATE INDEX IF NOT EXISTS idx_instances_account ON instances(account_id);
```

### 2.2 Adicionar Variáveis de Ambiente na Vercel

No dashboard da Vercel, vá em **Settings** > **Environment Variables** e adicione:

```
DB_HOST=db.xxxxx.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=SUA_SENHA_DO_SUPABASE
DB_PORT=5432
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=sua_anon_key
SUPABASE_SERVICE_KEY=sua_service_key
SECRET_KEY=qualquer_chave_aleatoria_segura
BOT_MODE=webjs
ENVIRONMENT=production
```

**Substitua:**
- `xxxxx` pelo ID do seu projeto Supabase
- `SUA_SENHA_DO_SUPABASE` pela senha do banco
- `sua_anon_key` pela anon public key
- `sua_service_key` pela service_role key

---

## 📱 Passo 3: WhatsApp Web.js (Servidor Separado)

⚠️ **IMPORTANTE:** WhatsApp Web.js **NÃO funciona** em serverless (Vercel).

Você precisa de um servidor separado:

### Opção A: Railway (Recomendado - Grátis)

1. Acesse: https://railway.app
2. **New Project** > **Deploy from GitHub repo**
3. Selecione seu repositório
4. Configure:
   - **Start Command**: `node whatsapp_server.js`
5. Adicione variáveis se necessário
6. Deploy!

### Opção B: Render (Alternativa - Grátis)

1. Acesse: https://render.com
2. **New** > **Web Service**
3. Conecte GitHub
4. Configure:
   - **Build Command**: `npm install`
   - **Start Command**: `node whatsapp_server.js`
5. Deploy!

---

## 🔄 Passo 4: Atualizar Código e Fazer Deploy

### 4.1 Atualizar Código Local

```bash
cd "/Users/air/Ylada BOT"

# Atualizar api/index.py para usar app_multi.py
# (ou criar api/index_multi.py)

# Fazer commit
git add .
git commit -m "Add multi-instance support"
git push
```

### 4.2 Deploy Automático

A Vercel vai fazer deploy automaticamente quando você fizer push!

---

## ✅ Passo 5: Configurar 4 Contas

Após o deploy, você precisa criar suas 4 contas. Você pode:

### Opção A: Via API (Recomendado)

```bash
# Criar conta 1
curl -X POST https://seu-projeto.vercel.app/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Conta 1",
    "phone": "5511999999999",
    "plan": "owner"
  }'

# Repetir para as outras 3 contas
```

### Opção B: Via SQL no Supabase

```sql
-- Criar 4 contas
INSERT INTO accounts (name, phone, plan) VALUES
    ('Conta 1', '5511999999999', 'owner'),
    ('Conta 2', '5511888888888', 'owner'),
    ('Conta 3', '5511777777777', 'owner'),
    ('Conta 4', '5511666666666', 'owner');

-- Criar 4 instâncias (uma por conta)
INSERT INTO instances (account_id, instance_name, port)
SELECT id, 'instance_' || phone, 
    CASE 
        WHEN phone = '5511999999999' THEN 5001
        WHEN phone = '5511888888888' THEN 5002
        WHEN phone = '5511777777777' THEN 5003
        WHEN phone = '5511666666666' THEN 5004
    END
FROM accounts;
```

---

## 🎯 Arquitetura Final:

```
┌─────────────────────────────────────┐
│         VERCEL (Backend/API)        │
│  - app_multi.py                     │
│  - Multi-instance endpoints         │
│  - Banco Supabase                   │
│  ✅ 24/7 - Sem computador ligado    │
└──────────────┬──────────────────────┘
               │
               │ API Calls
               │
┌──────────────▼──────────────────────┐
│    RAILWAY/RENDER (WhatsApp Web.js) │
│  - whatsapp_server.js               │
│  - 4 instâncias (portas diferentes) │
│  ✅ 24/7 - Sem computador ligado    │
└──────────────┬──────────────────────┘
               │
               │
┌──────────────▼──────────────────────┐
│      SUPABASE (Banco de Dados)      │
│  - PostgreSQL                        │
│  - Tabelas multi-tenant              │
│  ✅ 24/7 - Sem computador ligado    │
└─────────────────────────────────────┘
```

---

## 📋 Checklist:

- [ ] Atualizar `api/index.py` para usar `app_multi.py`
- [ ] Criar tabelas no Supabase
- [ ] Adicionar variáveis de ambiente na Vercel
- [ ] Deploy servidor WhatsApp Web.js (Railway/Render)
- [ ] Fazer commit e push (deploy automático)
- [ ] Criar 4 contas via API ou SQL
- [ ] Testar endpoints
- [ ] Conectar telefones via QR Code

---

## 🆘 Problemas Comuns:

### Erro: "Database connection failed"
- Verifique variáveis de ambiente na Vercel
- Confirme que as tabelas foram criadas no Supabase

### WhatsApp não conecta
- Verifique se o servidor Railway/Render está rodando
- Confirme que as portas estão corretas

### Deploy falha
- Veja logs na Vercel
- Verifique se todas as dependências estão no `requirements.txt`

---

## 🎉 Pronto!

Agora você tem:
- ✅ Backend na Vercel (24/7)
- ✅ WhatsApp Web.js no Railway/Render (24/7)
- ✅ Banco de dados no Supabase (24/7)
- ✅ **Tudo funciona sem seu computador ligado!**

Quer que eu atualize o `api/index.py` agora?

