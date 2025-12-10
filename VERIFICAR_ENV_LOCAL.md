# ✅ Verificação do .env.local

## 📋 Variáveis Necessárias:

### **Obrigatórias:**
- [ ] `DB_HOST` - Host do Supabase
- [ ] `DB_NAME` - Nome do banco (geralmente `postgres`)
- [ ] `DB_USER` - Usuário (geralmente `postgres`)
- [ ] `DB_PASSWORD` - Senha do Supabase
- [ ] `DB_PORT` - Porta (geralmente `5432`)
- [ ] `SUPABASE_URL` - URL do projeto Supabase
- [ ] `SUPABASE_KEY` - Anon key do Supabase
- [ ] `SUPABASE_SERVICE_KEY` - Service role key do Supabase
- [ ] `SECRET_KEY` - Chave secreta da aplicação
- [ ] `BOT_MODE=webjs` - Modo do bot
- [ ] `ENVIRONMENT=production` - Ambiente
- [ ] `PORT=5002` - Porta do Flask
- [ ] `RENDER_WHATSAPP_URL` - URL do servidor WhatsApp no Render

### **Valores Esperados:**
- `DB_HOST=db.tbbjqvvtsotjqgfygaaj.supabase.co`
- `DB_NAME=postgres`
- `DB_USER=postgres`
- `DB_PASSWORD=Afo@1974` (ou sua senha)
- `DB_PORT=5432`
- `SUPABASE_URL=https://tbbjqvvtsotjqgfygaaj.supabase.co`
- `SUPABASE_KEY=eyJ...` (chave longa)
- `SUPABASE_SERVICE_KEY=eyJ...` (chave longa)
- `SECRET_KEY=49073da7c373f1bd73340a345201ce20ecdf4d965dd1a2015ceac9f7870f2c28`
- `BOT_MODE=webjs`
- `ENVIRONMENT=production`
- `PORT=5002`
- `RENDER_WHATSAPP_URL=https://ylada-bot.onrender.com`

---

## ⚠️ Importante:

- **NÃO commitar** o `.env.local` no Git (já está no `.gitignore`)
- **Adicionar as mesmas variáveis** na Vercel também
- **SUPABASE_KEY e SUPABASE_SERVICE_KEY** precisam ser preenchidas com as chaves reais do Supabase

---

## 🔍 Como Verificar:

Execute no terminal:
```bash
cat .env.local | grep -E "^[A-Z_]+="
```

Isso mostra todas as variáveis definidas.



