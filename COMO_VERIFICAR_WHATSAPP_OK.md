# ✅ COMO VERIFICAR SE WHATSAPP ESTÁ OK

## 📋 VARIÁVEIS NO RAILWAY

### **Você PODE manter ambas:**

1. **`WHATSAPP_SERVICE_NAME`** = `whatsapp-server-2` ✅ **ESSENCIAL**
   - Esta é a mais importante agora
   - O código vai usar esta primeiro

2. **`WHATSAPP_SERVER_URL`** = `https://whatsapp-server-2-production.up.railway.app`
   - Você PODE deixar como está
   - Ou PODE remover (não é mais necessária)
   - O código agora prioriza `WHATSAPP_SERVICE_NAME`

**Recomendação:** Deixe ambas por enquanto. Não vai fazer mal.

---

## 🔍 ONDE VERIFICAR SE WHATSAPP ESTÁ OK

### **OPÇÃO 1: No Railway (Mais Fácil)**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. **Clique no serviço "whatsapp-server-2"** (card da esquerda)
4. Veja o status:
   - ✅ **"Online"** (bolinha verde) = Está rodando ✅
   - ❌ **"Crashed"** = Parou (veja logs)
   - ❌ **"Completed"** = Terminou (não deveria)

5. **Clique na aba "Logs"** (no topo)
   - Procure por mensagens como:
     - ✅ `Servidor WhatsApp Web.js rodando em http://localhost:5001`
     - ✅ `WhatsApp CONECTADO E PRONTO!`
     - ❌ Se aparecer erros, copie e me envie

---

### **OPÇÃO 2: Testar Diretamente (Avançado)**

1. No Railway, serviço "whatsapp-server-2"
2. **Settings** → **Networking**
3. Se tiver domínio público, copie a URL
4. Acesse no navegador: `https://seu-dominio.railway.app/health`
   - Deve retornar: `{"status":"ok","activeClients":X}`
   - Se retornar isso = ✅ Está funcionando!

---

### **OPÇÃO 3: Verificar no Dashboard**

1. Acesse: `https://yladabot.com/dashboard`
2. Veja a seção "WhatsApp":
   - ✅ **"Conectado"** (verde) = Está OK!
   - ❌ **"Desconectado"** (vermelho) = Precisa conectar
   - ⏳ **"Conectando..."** = Está tentando conectar

3. **Clique em "Conectar WhatsApp"**
   - Deve aparecer QR Code
   - Se aparecer = ✅ Servidor está funcionando!

---

## 🎯 RESUMO: O QUE VERIFICAR

### **1. Serviço WhatsApp está Online?**
- Railway → whatsapp-server-2 → Status = "Online" ✅

### **2. Variável está configurada?**
- Railway → ylada-bot → Variables → `WHATSAPP_SERVICE_NAME` = `whatsapp-server-2` ✅

### **3. QR Code aparece?**
- Acesse `yladabot.com/qr` → Deve aparecer QR Code ✅

### **4. Conecta após escanear?**
- Escaneie QR → Deve conectar em alguns segundos ✅

---

## ⚠️ SE AINDA NÃO FUNCIONAR

### **Verifique os Logs do Flask:**

1. Railway → ylada-bot → **Deployments** → **Logs**
2. Procure por:
   - `🔗 WHATSAPP_SERVICE_NAME configurado! Usando: http://whatsapp-server-2:5001`
   - Se aparecer isso = ✅ Está usando comunicação interna!
   - Se aparecer `localhost:5001` = ❌ Ainda não aplicou o deploy

### **Verifique os Logs do WhatsApp:**

1. Railway → whatsapp-server-2 → **Deployments** → **Logs**
2. Procure por:
   - `Servidor WhatsApp iniciado`
   - `WhatsApp CONECTADO`
   - Se aparecer erros, copie e me envie

---

## 📋 CHECKLIST RÁPIDO

- [ ] Serviço whatsapp-server-2 está "Online" no Railway?
- [ ] Variável WHATSAPP_SERVICE_NAME está configurada?
- [ ] QR Code aparece quando clica em "Conectar WhatsApp"?
- [ ] Logs do Flask mostram `http://whatsapp-server-2:5001` (não localhost)?
- [ ] Logs do WhatsApp mostram "Servidor iniciado"?

**Se todos estão ✅, está funcionando!**

---

**Última atualização:** 13/01/2026
