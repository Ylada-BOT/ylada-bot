# ✅ Configurar WHATSAPP_SERVER_URL - Final

## 🔗 URL DO SERVIÇO

Sua URL do serviço WhatsApp é:
```
https://whatsapp-server-2-production.up.railway.app
```

---

## ✅ CONFIGURAÇÃO NO SERVIÇO FLASK

### **Passo 1: Acessar Variables do Flask**

1. No Railway, clique no serviço **ylada-bot** (Flask)
2. Vá em **Variables**

### **Passo 2: Adicionar/Atualizar Variável**

1. Procure por `WHATSAPP_SERVER_URL`
2. Se existir, clique em **Edit**
3. Se não existir, clique em **+ New Variable**

4. Configure:
   - **Nome:** `WHATSAPP_SERVER_URL`
   - **Valor:** `https://whatsapp-server-2-production.up.railway.app`

5. Clique em **Save**

### **Passo 3: Aguardar Redeploy**

1. O Railway vai fazer redeploy automaticamente
2. Aguarde 1-2 minutos
3. Verifique os logs para confirmar

---

## 🔍 VERIFICAÇÃO

Após configurar, os logs do Flask devem mostrar:
- ✅ `WHATSAPP_SERVER_URL=https://whatsapp-server-2-production.up.railway.app`
- ✅ Consegue conectar no servidor WhatsApp

---

## 🚀 TESTAR

1. Aguarde o redeploy completar
2. Acesse: `https://yladabot.com/qr`
3. Deve funcionar agora! ✅

---

## 📋 CHECKLIST FINAL

- [ ] URL copiada: `https://whatsapp-server-2-production.up.railway.app`
- [ ] Variável `WHATSAPP_SERVER_URL` configurada no serviço `ylada-bot`
- [ ] Valor: `https://whatsapp-server-2-production.up.railway.app`
- [ ] Salvei as alterações
- [ ] Aguardei redeploy
- [ ] Testei acessando `/qr`

---

**Última atualização:** 27/01/2025

