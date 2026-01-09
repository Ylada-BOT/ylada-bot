# 🔧 Serviço Não Inicia no Railway

## ⚠️ PROBLEMA

O serviço `whatsapp-server-2` não está iniciando no Railway.

---

## 🔍 DIAGNÓSTICO

### **1. Verificar Status do Serviço**

1. No Railway, clique no serviço `whatsapp-server-2`
2. Veja o status:
   - ❌ **"Crashed"** = Está crashando
   - ⚠️ **"Completed"** = Terminou (não deveria)
   - ✅ **"Online"** = Está rodando (bom!)

### **2. Verificar Logs**

1. Vá em **Deployments** → Último deploy
2. Clique nos **Logs**
3. Procure por:
   - ❌ Erros de inicialização
   - ❌ "Command not found"
   - ❌ "Cannot find module"
   - ❌ "Port already in use"
   - ✅ "Servidor WhatsApp iniciado" (se estiver funcionando)

---

## ✅ SOLUÇÕES COMUNS

### **Problema 1: Start Command Errado**

**Sintoma nos logs:**
- `bash start_app.sh` (erro - isso é para Python)
- "Command not found: node"

**Solução:**
1. **Settings** → **Deploy**
2. Verifique **Start Command**:
   - Deve ser: `node whatsapp_server.js`
   - OU: `npm start`
3. **Salve** e faça **Redeploy**

---

### **Problema 2: Build Command Faltando**

**Sintoma nos logs:**
- "Cannot find module 'whatsapp-web.js'"
- "Cannot find module 'express'"

**Solução:**
1. **Settings** → **Deploy**
2. Verifique **Build Command**:
   - Deve ser: `npm install`
3. **Salve** e faça **Redeploy**

---

### **Problema 3: Variável PORT Não Configurada**

**Sintoma nos logs:**
- "Port already in use"
- Servidor não inicia

**Solução:**
1. **Settings** → **Variables**
2. Adicione:
   ```bash
   PORT=5001
   ```
3. **Salve** e faça **Redeploy**

---

### **Problema 4: Railway Config File Não Configurado**

**Sintoma:**
- Railway detecta como Python
- Start Command volta para `bash start_app.sh`

**Solução:**
1. **Settings** → **Deploy**
2. No campo **"Railway Config File"**, digite: `railway.whatsapp.json`
3. **Salve** e faça **Redeploy**

---

## 🚀 CONFIGURAÇÃO CORRETA COMPLETA

### **Settings → Deploy:**

- **Railway Config File:** `railway.whatsapp.json`
- **Build Command:** `npm install` (se não usar config file)
- **Start Command:** `node whatsapp_server.js` (se não usar config file)

### **Settings → Variables:**

```bash
PORT=5001
NODE_ENV=production
```

### **Settings → Build → Providers:**

- ✅ **Node** (selecionado)
- ❌ **Python** (removido)

---

## 📋 CHECKLIST

- [ ] Status do serviço verificado
- [ ] Logs verificados (último deploy)
- [ ] Railway Config File: `railway.whatsapp.json`
- [ ] Start Command correto (ou usando config file)
- [ ] Build Command: `npm install`
- [ ] Variável `PORT=5001` configurada
- [ ] Provider Python removido (só Node)
- [ ] Redeploy feito

---

## 🔍 O QUE PROCURAR NOS LOGS

### **✅ Bom (Servidor Iniciou):**
```
✅ Build: npm install (sucesso)
✅ Start: node whatsapp_server.js
🚀 Servidor WhatsApp Web.js rodando em http://localhost:5001
📱 Client ID: ylada_bot_5001
```

### **❌ Ruim (Erros Comuns):**

**Erro 1: Command not found**
```
/bin/sh: node: command not found
```
→ **Solução:** Configure Railway Config File ou Start Command manualmente

**Erro 2: Module not found**
```
Cannot find module 'whatsapp-web.js'
```
→ **Solução:** Adicione Build Command: `npm install`

**Erro 3: Port in use**
```
Port 5001 is already in use
```
→ **Solução:** Verifique variável PORT ou mude para outra porta

**Erro 4: Wrong command**
```
bash start_app.sh
```
→ **Solução:** Railway está detectando como Python. Use Railway Config File.

---

## 💡 DICA RÁPIDA

**Se nada funcionar:**

1. **Delete o serviço** `whatsapp-server-2`
2. **Crie um novo** serviço vazio
3. **Configure tudo do zero:**
   - Railway Config File: `railway.whatsapp.json`
   - Variables: `PORT=5001`
4. **Faça deploy**

---

**Última atualização:** 27/01/2025

