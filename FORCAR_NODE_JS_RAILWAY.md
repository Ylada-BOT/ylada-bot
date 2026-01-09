# 🔧 Forçar Railway a Usar Node.js (não Python)

## ⚠️ PROBLEMA

O Railway está detectando automaticamente como **Python** e mudando o Start Command de volta para `bash start_app.sh`, mesmo depois de você salvar.

---

## ✅ SOLUÇÃO: USAR ARQUIVO DE CONFIGURAÇÃO

### **Opção 1: Usar railway.whatsapp.json (Recomendado)**

1. No Railway, no serviço `whatsapp-server-2`
2. Vá em **Settings** → **Deploy**
3. Role até encontrar **"Railway Config File"** ou **"Config File"**
4. Digite: `railway.whatsapp.json`
5. Clique em **Save**
6. Vá em **Deployments** → **Redeploy**

Isso vai forçar o Railway a usar a configuração do arquivo, que está correta para Node.js.

---

### **Opção 2: Configurar Manualmente e Remover Providers Python**

1. **Settings** → **Deploy**:
   - **Build Command:** `npm install`
   - **Start Command:** `node whatsapp_server.js`
   - **Pre-deploy Command:** (deixe vazio ou remova `npm run migrate`)

2. **Settings** → **Build**:
   - Veja a seção **"Providers"**
   - **Remova** o provider **Python** (se estiver lá)
   - Deixe apenas **Node** selecionado

3. **Salve** e faça **Redeploy**

---

### **Opção 3: Renomear Arquivo Temporariamente**

Se o Railway está detectando Python por causa do `requirements.txt` ou outros arquivos:

1. **Temporariamente**, renomeie ou mova:
   - `requirements.txt` → `requirements.txt.bak`
   - `start_app.sh` → `start_app.sh.bak`

2. **Faça commit e push** (ou apenas salve no Railway)

3. **Railway vai detectar apenas Node.js**

4. **Depois**, pode renomear de volta

---

## 🔍 VERIFICAÇÕES

### **Checklist:**

- [ ] Railway Config File: `railway.whatsapp.json`
- [ ] Build Command: `npm install`
- [ ] Start Command: `node whatsapp_server.js`
- [ ] Providers: Apenas **Node** (não Python)
- [ ] Variável `PORT=5001` configurada
- [ ] Variável `WHATSAPP_SERVER_URL` configurada no `ylada-bot`

---

## 📋 CONFIGURAÇÃO FINAL CORRETA

### **Serviço whatsapp-server-2:**

**Settings → Deploy:**
- Railway Config File: `railway.whatsapp.json`
- OU manualmente:
  - Build Command: `npm install`
  - Start Command: `node whatsapp_server.js`

**Settings → Variables:**
```bash
PORT=5001
NODE_ENV=production
```

**Settings → Build → Providers:**
- ✅ Node (selecionado)
- ❌ Python (removido)

### **Serviço ylada-bot (Flask):**

**Settings → Variables:**
```bash
WHATSAPP_SERVER_URL=https://whatsapp-server-2.railway.app
```
(Substitua pela URL real do seu serviço)

---

## 🚀 PRÓXIMOS PASSOS

1. **Configure Railway Config File:** `railway.whatsapp.json`
2. **OU remova provider Python** e configure manualmente
3. **Salve e faça Redeploy**
4. **Verifique logs** - deve aparecer "Servidor WhatsApp iniciado"
5. **Teste** acessando `/qr`

---

**Última atualização:** 27/01/2025

