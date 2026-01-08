# ✅ Correção: whatsapp-server-2 Crashed no Railway

**Data:** 2025-01-27  
**Problema:** Serviço `whatsapp-server-2` está usando comando Python em vez de Node.js  
**Status:** ✅ Solução documentada

---

## 🐛 PROBLEMA

O serviço `whatsapp-server-2` no Railway está configurado para executar:
```bash
bash start_app.sh  # ❌ Este é para Python/Flask!
```

Mas este é um serviço **Node.js** que precisa executar:
```bash
node whatsapp_server.js  # ✅ Correto!
```

**Resultado:** O serviço crasha porque tenta executar um script Python em um serviço Node.js.

---

## ✅ SOLUÇÃO

### **Opção 1: Configurar Manualmente no Railway (RECOMENDADO)**

No Railway, cada serviço pode ter sua própria configuração:

1. Acesse o serviço `whatsapp-server-2` no Railway
2. Vá em **Settings** → **Deploy**
3. Altere o **Start Command** para:
   ```bash
   node whatsapp_server.js
   ```
4. Salve e faça redeploy

### **Opção 2: Usar Arquivo de Configuração Específico**

Criei o arquivo `railway.whatsapp.json` que pode ser usado para serviços Node.js.

**Como usar:**
1. No Railway, no serviço `whatsapp-server-2`
2. Vá em **Settings** → **Deploy**
3. Em **Railway Config File**, especifique: `railway.whatsapp.json`
4. Salve e faça redeploy

---

## 📋 CONFIGURAÇÃO CORRETA

### **Para Serviço Python (Flask):**
- **Start Command:** `bash start_app.sh` ou `python web/app.py`
- **Build Command:** `pip install -r requirements.txt`

### **Para Serviço Node.js (WhatsApp):**
- **Start Command:** `node whatsapp_server.js`
- **Build Command:** `npm install` ou `npm ci`

---

## 🔧 PASSOS PARA CORRIGIR AGORA

### **1. No Railway Dashboard:**

1. Acesse: https://railway.app/dashboard
2. Selecione o projeto
3. Clique no serviço `whatsapp-server-2`
4. Vá em **Settings** → **Deploy**
5. Altere **Start Command** para: `node whatsapp_server.js`
6. Clique em **Save**
7. Vá em **Deployments** → **Redeploy**

### **2. Verificar Variáveis de Ambiente:**

No serviço `whatsapp-server-2`, verifique se tem:
```bash
PORT=5001
NODE_ENV=production
```

### **3. Verificar Logs:**

Após o redeploy, verifique os logs. Deve aparecer:
```
🚀 Servidor WhatsApp Web.js rodando em http://localhost:5001
📱 Client ID: ylada_bot_5001
🔄 Auto-reconexão: ATIVADA
```

---

## 📊 ESTRUTURA DE SERVIÇOS NO RAILWAY

### **Serviço 1: Flask (Python)**
- **Nome:** `web` ou `flask-app`
- **Start Command:** `bash start_app.sh`
- **Port:** `5002`
- **Arquivo:** `railway.json` (padrão)

### **Serviço 2: WhatsApp (Node.js)**
- **Nome:** `whatsapp-server-2` ou `whatsapp-server`
- **Start Command:** `node whatsapp_server.js`
- **Port:** `5001`
- **Arquivo:** `railway.whatsapp.json` (opcional)

---

## ✅ CHECKLIST

- [ ] Acessar serviço `whatsapp-server-2` no Railway
- [ ] Ir em **Settings** → **Deploy**
- [ ] Alterar **Start Command** para `node whatsapp_server.js`
- [ ] Verificar variável `PORT=5001` em **Variables**
- [ ] Fazer **Redeploy**
- [ ] Verificar logs - deve iniciar corretamente
- [ ] Testar endpoint `/health` do serviço

---

## 🔍 VERIFICAÇÃO

Após corrigir, os logs devem mostrar:

```
✅ Build: npm ci (sucesso)
✅ Start: node whatsapp_server.js
✅ Servidor rodando na porta 5001
✅ Auto-reconexão ativada
```

**Se ainda crashar, verifique:**
1. Logs completos do deploy
2. Se `whatsapp_server.js` existe no repositório
3. Se `package.json` tem as dependências corretas
4. Se a porta `5001` está configurada

---

## 📝 NOTAS

- O `railway.json` padrão é para o serviço Python
- Cada serviço no Railway pode ter configuração diferente
- O comando de start pode ser configurado manualmente no dashboard
- O arquivo `railway.whatsapp.json` é opcional, mas útil para referência

---

**Última atualização:** 2025-01-27  
**Status:** ✅ **SOLUÇÃO DOCUMENTADA - CONFIGURAR MANUALMENTE NO RAILWAY**

