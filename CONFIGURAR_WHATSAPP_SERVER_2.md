# 🔧 Configurar whatsapp-server-2 no Railway

## ✅ SERVIÇO EXISTE

Você tem o serviço `whatsapp-server-2` no Railway, mas ele precisa estar configurado corretamente.

---

## 🔍 VERIFICAÇÕES NECESSÁRIAS

### **1. Verificar Status do Serviço**

1. No Railway, clique no serviço `whatsapp-server-2`
2. Veja o status:
   - ✅ **"Online"** = Está rodando (bom!)
   - ⚠️ **"Completed"** = Terminou (pode estar crashando)
   - ❌ **"Crashed"** = Está com erro

### **2. Verificar Configuração**

1. No serviço `whatsapp-server-2`, vá em **Settings** → **Deploy**
2. Verifique:
   - **Build Command:** Deve ser `npm install`
   - **Start Command:** Deve ser `node whatsapp_server.js`
   - **Providers:** Deve ter apenas **Node** (não Python)

### **3. Verificar Variáveis de Ambiente**

1. No serviço `whatsapp-server-2`, vá em **Variables**
2. Deve ter:
   ```bash
   PORT=5001
   NODE_ENV=production
   ```

### **4. Verificar Logs**

1. No serviço `whatsapp-server-2`, vá em **Deployments**
2. Clique no último deploy
3. Veja os logs
4. Procure por:
   - ✅ `Servidor WhatsApp iniciado`
   - ✅ `Rodando na porta 5001`
   - ❌ Erros de inicialização
   - ❌ "Crashed" ou "Failed"

---

## ✅ CONFIGURAR URL NO SERVIÇO FLASK

### **Passo 1: Obter URL do Serviço WhatsApp**

1. No serviço `whatsapp-server-2`, vá em **Settings** → **Networking**
2. Veja se há um domínio gerado
3. Se não houver, clique em **"Generate Domain"**
4. Copie a URL (ex: `https://whatsapp-server-2.railway.app`)

### **Passo 2: Configurar no Serviço Flask**

1. No Railway, selecione o serviço **ylada-bot** (Flask)
2. Vá em **Variables**
3. Adicione ou atualize:
   ```bash
   WHATSAPP_SERVER_URL=https://whatsapp-server-2.railway.app
   ```
   (Substitua pela URL real do seu serviço)
4. Salve e aguarde redeploy

---

## 🔧 CORRIGIR SE ESTIVER CRASHANDO

### **Se o serviço está "Completed" ou "Crashed":**

1. **Verifique os logs** para ver o erro
2. **Verifique o Start Command:**
   - Deve ser: `node whatsapp_server.js`
   - NÃO deve ser: `bash start_app.sh` (isso é para Python)
3. **Verifique o Build Command:**
   - Deve ser: `npm install`
4. **Verifique as variáveis:**
   - `PORT=5001`
   - `NODE_ENV=production`

### **Se o Start Command estiver errado:**

1. Settings → Deploy
2. Altere **Start Command** para: `node whatsapp_server.js`
3. Salve
4. Vá em Deployments → **Redeploy**

---

## 📋 CHECKLIST

- [ ] Serviço `whatsapp-server-2` está "Online" (não "Completed" ou "Crashed")
- [ ] Start Command: `node whatsapp_server.js`
- [ ] Build Command: `npm install`
- [ ] Variável `PORT=5001` configurada
- [ ] Domínio gerado (Networking)
- [ ] `WHATSAPP_SERVER_URL` configurada no serviço `ylada-bot`
- [ ] Logs mostram "Servidor WhatsApp iniciado"

---

## 🚀 PRÓXIMOS PASSOS

1. **Verifique o status** do serviço `whatsapp-server-2`
2. **Se estiver "Completed" ou "Crashed":**
   - Veja os logs
   - Corrija o Start Command se necessário
   - Faça redeploy
3. **Configure a URL** no serviço `ylada-bot`
4. **Teste novamente** acessando `/qr`

---

**Última atualização:** 27/01/2025

