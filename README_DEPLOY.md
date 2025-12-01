# 🚀 Deploy Rápido - Ylada BOT

## ⚡ Passo a Passo Simplificado

### 1️⃣ Preparar GitHub

```bash
# Se ainda não inicializou
git init
git add .
git commit -m "Ylada BOT - Ready for deploy"

# Conectar ao seu repositório GitHub
git remote add origin https://github.com/SEU-USUARIO/ylada-bot.git
git push -u origin main
```

### 2️⃣ Configurar Supabase

1. Acesse: https://app.supabase.com
2. Crie novo projeto
3. Vá em **SQL Editor** e execute o script em `DEPLOY.md` (seção 1.2)
4. Vá em **Settings** > **API** e copie:
   - Project URL
   - anon public key
   - service_role key

### 3️⃣ Deploy na Vercel

1. Acesse: https://vercel.com
2. **Add New Project**
3. Importe seu repositório GitHub
4. Configure:
   - Framework: **Other**
   - Root Directory: `.`
5. Adicione variáveis de ambiente:
   ```
   SUPABASE_URL=sua_url
   SUPABASE_KEY=sua_key
   SUPABASE_SERVICE_KEY=sua_service_key
   SECRET_KEY=qualquer_chave_aleatoria_segura
   BOT_MODE=webjs
   ENVIRONMENT=production
   ```
6. **Deploy** 🚀

### 4️⃣ Pronto!

Seu bot estará em: `https://seu-projeto.vercel.app`

## 📝 Próximos Passos

Após deploy, configure:
- Domínio personalizado (opcional)
- Servidor para WhatsApp Web.js (Railway/Render)

## ❓ Problemas?

Veja `DEPLOY.md` para guia completo e troubleshooting.

