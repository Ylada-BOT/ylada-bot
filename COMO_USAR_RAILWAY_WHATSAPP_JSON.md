# 🔧 Como Usar railway.whatsapp.json no Railway

## ⚠️ PROBLEMA

O Railway está detectando automaticamente como **Python** e mudando o Start Command de volta para `bash start_app.sh`, mesmo depois de salvar.

---

## ✅ SOLUÇÃO: USAR ARQUIVO DE CONFIGURAÇÃO

### **PASSO 1: Usar railway.whatsapp.json**

1. No Railway, no serviço `whatsapp-server-2`
2. Vá em **Settings** → **Deploy**
3. Role até encontrar o campo **"Railway Config File"** ou **"Config File"**
4. Digite exatamente: `railway.whatsapp.json`
5. Clique em **Save** ou **Apply**

**Isso vai forçar o Railway a usar a configuração do arquivo!**

---

### **PASSO 2: Verificar Configuração**

O arquivo `railway.whatsapp.json` está configurado com:
- **Start Command:** `node whatsapp_server.js` ✅

Isso vai sobrescrever qualquer detecção automática do Railway.

---

### **PASSO 3: Fazer Redeploy**

1. Vá em **Deployments**
2. Clique em **Redeploy** (ou aguarde deploy automático)
3. Aguarde completar
4. Verifique os logs

---

## 🔍 VERIFICAÇÃO

Após configurar, os logs devem mostrar:

```
✅ Build: npm install (sucesso)
✅ Start: node whatsapp_server.js
✅ Servidor WhatsApp iniciado na porta 5001
```

**NÃO deve aparecer:**
- ❌ `bash start_app.sh`
- ❌ Erros de Python
- ❌ "Command not found"

---

## 📋 CHECKLIST

- [ ] Railway Config File: `railway.whatsapp.json` configurado
- [ ] Salvei as alterações
- [ ] Fiz redeploy
- [ ] Logs mostram "node whatsapp_server.js"
- [ ] Servidor está rodando (não crashando)

---

## 💡 DICA

Se ainda não funcionar:

1. **Remova o provider Python:**
   - Settings → Build → Providers
   - Remova **Python** (deixe apenas **Node**)

2. **Ou renomeie temporariamente:**
   - `requirements.txt` → `requirements.txt.bak`
   - Isso faz o Railway detectar apenas Node.js

---

**Última atualização:** 27/01/2025

