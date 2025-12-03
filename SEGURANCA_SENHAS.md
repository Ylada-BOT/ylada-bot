# 🔒 Segurança - Proteção de Senhas e Credenciais

## ⚠️ IMPORTANTE: NUNCA commite senhas no Git!

---

## ✅ Arquivos PROTEGIDOS (não serão commitados):

Estes arquivos estão no `.gitignore` e **NÃO serão commitados**:

- ✅ `.env.local` - Suas variáveis locais com senhas
- ✅ `VARIAVEIS_VERCEL_COMPLETO.txt` - Arquivo com senhas
- ✅ `VARIAVEIS_SEU_PROJETO.txt` - Arquivo com senhas
- ✅ Qualquer arquivo `*_COMPLETO.txt` ou `*_SEU_PROJETO.txt`

---

## 📋 O que fazer:

### **1. Arquivo `.env.local` (LOCAL apenas)**

✅ **NÃO commitar** - Já está protegido no `.gitignore`

Este arquivo é só para você usar localmente. **NUNCA** faça commit dele!

### **2. Arquivo `VARIAVEIS_VERCEL_COMPLETO.txt`**

⚠️ **NÃO commitar** - Já está protegido no `.gitignore`

Este arquivo tem senhas. Use apenas para copiar valores para a Vercel, depois **delete ou não commite**.

### **3. Variáveis na Vercel**

✅ **Seguro** - As variáveis na Vercel são privadas e não aparecem no código

Você adiciona as variáveis diretamente no dashboard da Vercel (Settings → Environment Variables). Elas ficam seguras lá.

---

## 🚨 Checklist de Segurança:

Antes de fazer commit, verifique:

- [ ] `.env.local` **NÃO** está no commit
- [ ] Arquivos com senhas **NÃO** estão no commit
- [ ] `VARIAVEIS_VERCEL_COMPLETO.txt` **NÃO** está no commit
- [ ] Senhas estão apenas na Vercel (Environment Variables)

---

## ✅ Como fazer commit seguro:

```bash
# Verificar o que vai ser commitado
git status

# Se aparecer .env.local ou arquivos com senhas:
# NÃO faça commit! Eles devem estar no .gitignore

# Fazer commit apenas dos arquivos de código
git add .
git commit -m "Update code"
git push
```

---

## 🔐 Onde colocar senhas:

### **Local (desenvolvimento):**
- ✅ `.env.local` (não commitar)

### **Produção (Vercel):**
- ✅ Environment Variables no dashboard da Vercel
- ✅ **NÃO** no código
- ✅ **NÃO** em arquivos commitados

---

## ⚠️ Se você acidentalmente commitou senhas:

1. **Remova do histórico:**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.local VARIAVEIS_VERCEL_COMPLETO.txt" \
  --prune-empty --tag-name-filter cat -- --all
```

2. **Force push (cuidado!):**
```bash
git push origin --force --all
```

3. **Mude as senhas:**
   - Mude a senha do banco no Supabase
   - Gere novas chaves API no Supabase
   - Atualize na Vercel

---

## ✅ Resumo:

- ✅ `.env.local` = Só local, não commitar
- ✅ Vercel Environment Variables = Seguro, não aparece no código
- ❌ **NUNCA** commite arquivos com senhas reais
- ✅ `.gitignore` já protege os arquivos sensíveis

---

**Agora você pode fazer commit e deploy com segurança!** 🔒

