# ✅ Checklist de Deploy

## 📋 Antes de Fazer Deploy

### ✅ Preparação do Código
- [x] `.gitignore` criado
- [x] `vercel.json` configurado
- [x] `requirements.txt` atualizado
- [x] `api/index.py` criado
- [x] Cliente Supabase criado (`src/supabase_client.py`)

### 📦 Git e GitHub
- [ ] Repositório Git inicializado
- [ ] Código commitado
- [ ] Repositório GitHub criado
- [ ] Código enviado para GitHub

### 🗄️ Supabase
- [ ] Projeto criado no Supabase
- [ ] Tabelas criadas (SQL executado)
- [ ] URL e Keys copiadas

### 🚀 Vercel
- [ ] Projeto criado no Vercel
- [ ] Repositório GitHub conectado
- [ ] Variáveis de ambiente configuradas:
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_KEY`
  - [ ] `SUPABASE_SERVICE_KEY`
  - [ ] `SECRET_KEY`
  - [ ] `BOT_MODE=webjs`
  - [ ] `ENVIRONMENT=production`
- [ ] Deploy executado
- [ ] URL do deploy anotada

### 🧪 Testes Pós-Deploy
- [ ] Endpoint `/health` funcionando
- [ ] Dashboard acessível
- [ ] Conexão com Supabase testada
- [ ] Logs verificados no Vercel

## 📝 Comandos Úteis

```bash
# Inicializar Git
git init
git add .
git commit -m "Ylada BOT - Ready for deploy"

# Conectar GitHub
git remote add origin https://github.com/SEU-USUARIO/ylada-bot.git
git push -u origin main

# Verificar status
git status
```

## 🔗 Links Importantes

- **Vercel**: https://vercel.com/dashboard
- **Supabase**: https://app.supabase.com
- **GitHub**: https://github.com

## ⚠️ Lembretes

1. **WhatsApp Web.js** precisa de servidor separado (não funciona em serverless)
2. **Supabase** tem limite gratuito de 500MB
3. **Vercel** tem limite de 10s por função (hobby plan)
4. Guarde as **keys** em local seguro

