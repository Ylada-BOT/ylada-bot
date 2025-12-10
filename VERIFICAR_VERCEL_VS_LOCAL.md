# 🔍 Verificação: Vercel vs .env.local

## 📋 Variáveis que DEVEM estar na Vercel:

### **Banco de Dados (5 variáveis):**
- ✅ `DB_HOST`
- ✅ `DB_NAME`
- ✅ `DB_USER`
- ✅ `DB_PASSWORD`
- ✅ `DB_PORT`

### **Supabase API (3 variáveis):**
- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_KEY`
- ✅ `SUPABASE_SERVICE_KEY`

### **Aplicação (4 variáveis):**
- ✅ `SECRET_KEY`
- ✅ `BOT_MODE`
- ✅ `ENVIRONMENT`
- ✅ `PORT`

### **WhatsApp/Render (2 variáveis):**
- ✅ `RENDER_WHATSAPP_URL`
- ⚠️ `WHATSAPP_SERVER_PORT` (opcional, mas pode ser útil)

### **GitHub (1 variável - opcional):**
- ⚠️ `GITHUB_TOKEN` (opcional, só se usar GitHub API)

---

## ✅ O que você TEM na Vercel (da imagem):

1. ✅ `SUPABASE_KEY`
2. ✅ `SUPABASE_SERVICE_KEY`
3. ✅ `SECRET_KEY`
4. ✅ `BOT_MODE`
5. ✅ `ENVIRONMENT`
6. ✅ `PORT`
7. ✅ `RENDER_WHATSAPP_URL`
8. ✅ `DB_PASSWORD`
9. ✅ `DB_HOST`
10. ✅ `DB_NAME`
11. ✅ `DB_USER`
12. ✅ `DB_PORT`

**Total: 12 variáveis**

---

## ⚠️ O que PODE estar faltando:

### **Verifique se tem:**
- [ ] `SUPABASE_URL` - **IMPORTANTE!** Deve estar lá
- [ ] `WHATSAPP_SERVER_PORT` - Opcional (pode adicionar se quiser)
- [ ] `GITHUB_TOKEN` - Opcional (só se usar GitHub API)

---

## 🎯 Variáveis que NÃO precisam estar na Vercel:

### **Remover se encontrar:**
- ❌ `NODE_ENV` (use `ENVIRONMENT` ao invés)
- ❌ `FLASK_PORT` (use `PORT` ao invés)
- ❌ `SUPABASE_ANON_KEY` (use `SUPABASE_KEY` ao invés)
- ❌ `SUPABASE_SERVICE_ROLE_KEY` (use `SUPABASE_SERVICE_KEY` ao invés)
- ❌ `WHATSAPP_SERVER_URL` (use `RENDER_WHATSAPP_URL` ao invés)
- ❌ Qualquer variável com nome diferente dos listados acima

---

## ✅ Checklist Final:

### **Obrigatórias (12 variáveis):**
- [ ] `DB_HOST`
- [ ] `DB_NAME`
- [ ] `DB_USER`
- [ ] `DB_PASSWORD`
- [ ] `DB_PORT`
- [ ] `SUPABASE_URL` ⚠️ **VERIFIQUE SE ESTÁ LÁ!**
- [ ] `SUPABASE_KEY`
- [ ] `SUPABASE_SERVICE_KEY`
- [ ] `SECRET_KEY`
- [ ] `BOT_MODE`
- [ ] `ENVIRONMENT`
- [ ] `PORT`
- [ ] `RENDER_WHATSAPP_URL`

### **Opcionais (podem adicionar se quiser):**
- [ ] `WHATSAPP_SERVER_PORT=5001`
- [ ] `GITHUB_TOKEN` (só se usar GitHub API)

---

## 🔧 Ações Recomendadas:

1. **Verificar se `SUPABASE_URL` está na Vercel**
   - Se não estiver, adicione: `https://tbbjqvvtsotjqgfygaaj.supabase.co`

2. **Remover variáveis com nomes errados** (se houver)
   - Ex: `SUPABASE_ANON_KEY` → Deletar e usar `SUPABASE_KEY`

3. **Adicionar opcionais** (se quiser):
   - `WHATSAPP_SERVER_PORT=5001`
   - `GITHUB_TOKEN` (se usar GitHub API)

---

## 📝 Resumo:

**Você tem 12 variáveis na Vercel.**
**Falta verificar:** `SUPABASE_URL` (muito importante!)

**Tudo mais parece estar correto!** ✅



