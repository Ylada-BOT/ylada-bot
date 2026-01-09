# ✅ Solução: Erro "Invalid URL - No scheme supplied"

## 🐛 PROBLEMA IDENTIFICADO

O erro mostra:
```
Invalid URL 'whatsapp-server-2-production.up.railway.app/status': No scheme supplied. 
Perhaps you meant https://whatsapp-server-2-production.up.railway.app/status?
```

**Causa:** A URL estava sendo construída sem o protocolo `https://` no início.

---

## ✅ SOLUÇÃO APLICADA

Corrigi a função `get_whatsapp_server_url` em `web/utils/instance_helper.py` para:

1. **Detectar se a URL não tem protocolo**
2. **Adicionar `https://` automaticamente** se faltar
3. **Garantir que sempre retorne uma URL válida**

---

## 🚀 PRÓXIMOS PASSOS

### **1. Fazer Deploy da Correção**

```bash
git add web/utils/instance_helper.py
git commit -m "Corrigir URL do WhatsApp server - adicionar protocolo https:// automaticamente"
git push
```

### **2. Aguardar Redeploy no Railway**

- O Railway vai fazer deploy automaticamente
- Aguarde 1-2 minutos

### **3. Verificar Configuração**

Certifique-se de que a variável `WHATSAPP_SERVER_URL` está configurada no serviço Flask:

**No Railway → Serviço `ylada-bot` → Variables:**

```bash
WHATSAPP_SERVER_URL=https://whatsapp-server-2-production.up.railway.app
```

**OU** (se preferir comunicação interna):

```bash
WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001
```

---

## 🔍 VERIFICAÇÃO

Após o deploy, o erro deve desaparecer e você deve ver:

- ✅ Status do WhatsApp funcionando
- ✅ Sem erros "Invalid URL" no console
- ✅ Conexão com servidor WhatsApp estabelecida

---

## 📋 CHECKLIST

- [ ] Correção aplicada no código
- [ ] Commit e push feitos
- [ ] Aguardei deploy no Railway
- [ ] `WHATSAPP_SERVER_URL` configurada corretamente
- [ ] Testei novamente e erro desapareceu

---

**Última atualização:** 27/01/2025

