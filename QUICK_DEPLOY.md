# ⚡ Deploy Rápido - 5 Minutos

## 🎯 Passo a Passo Simplificado

### 1️⃣ Preparar Código (2 min)

```bash
# Execute o script de setup
./setup_deploy.sh

# Adicione tudo ao Git
git add .
git commit -m "Ready for deploy"
```

### 2️⃣ Subir para GitHub (1 min)

```bash
# Se ainda não tem repositório, crie no GitHub primeiro
# Depois conecte:
git remote add origin https://github.com/SEU-USUARIO/ylada-bot.git
git branch -M main
git push -u origin main
```

### 3️⃣ Configurar Supabase (1 min)

1. Acesse: https://app.supabase.com
2. **New Project** → Crie projeto
3. **SQL Editor** → Cole o SQL abaixo:

```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    tags TEXT[]
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    from_me BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    message TEXT,
    participants INTEGER DEFAULT 0,
    executions INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

4. **Settings** > **API** → Copie:
   - Project URL
   - anon public key

### 4️⃣ Deploy Vercel (1 min)

1. Acesse: https://vercel.com
2. **Add New Project**
3. Importe seu repositório
4. Configure:
   - Framework: **Other**
   - Root: `.`
5. **Environment Variables** → Adicione:
   ```
   SUPABASE_URL=sua_url_aqui
   SUPABASE_KEY=sua_key_aqui
   SECRET_KEY=qualquer_chave_aleatoria
   BOT_MODE=webjs
   ```
6. **Deploy** 🚀

### 5️⃣ Pronto! ✅

Seu bot estará em: `https://seu-projeto.vercel.app`

## 🔍 Testar

Acesse: `https://seu-projeto.vercel.app/health`

Deve retornar: `{"status": "ok", "bot": "Ylada BOT"}`

## 📝 Notas

- WhatsApp Web.js precisa de servidor separado (Railway/Render)
- Veja `DEPLOY.md` para guia completo

