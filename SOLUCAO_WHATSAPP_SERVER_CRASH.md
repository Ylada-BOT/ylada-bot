# 🔧 Solução: whatsapp-server-2 Crashed no Railway

**Problema:** Serviço `whatsapp-server-2` está crashando após deploy  
**Status:** ⚠️ Precisa configurar manualmente no Railway

---

## 🐛 PROBLEMA IDENTIFICADO

O serviço `whatsapp-server-2` está crashando porque:

1. **Start Command incorreto** - Pode estar usando `bash start_app.sh` (para Python) em vez de `node whatsapp_server.js`
2. **Build Command faltando** - Dependências Node.js não estão sendo instaladas
3. **Variável PORT não configurada** - Servidor não sabe em qual porta rodar

---

## ✅ SOLUÇÃO RÁPIDA

### **Passo 1: Acessar Settings do Serviço**

1. No Railway Dashboard, clique no serviço `whatsapp-server-2`
2. Vá em **Settings** → **Deploy**

### **Passo 2: Configurar Build Command**

No campo **Build Command**, adicione:
```bash
npm install
```

### **Passo 3: Configurar Start Command**

No campo **Custom Start Command**, altere para:
```bash
node whatsapp_server.js
```

**OU** use o script do package.json:
```bash
npm start
```

### **Passo 4: Configurar Variáveis de Ambiente**

Vá em **Variables** e adicione:

```bash
PORT=5001
NODE_ENV=production
```

### **Passo 5: Usar Arquivo de Configuração (Opcional)**

Se preferir usar arquivo de configuração:

1. Em **Settings** → **Deploy**
2. No campo **Railway Config File**, especifique: `railway.whatsapp.json`
3. Isso vai usar a configuração do arquivo automaticamente

### **Passo 6: Aplicar e Redeploy**

1. Clique em **"Apply changes"** ou **"Save"**
2. Vá em **Deployments** → **Redeploy**
3. Aguarde o deploy completar
4. Verifique os logs para confirmar que está rodando

---

## 📋 CONFIGURAÇÃO CORRETA FINAL

### **Build Command:**
```bash
npm install
```

### **Start Command:**
```bash
node whatsapp_server.js
```

**OU**

```bash
npm start
```

### **Variáveis de Ambiente:**
```bash
PORT=5001
NODE_ENV=production
```

---

## 🔍 VERIFICAÇÃO

Após configurar, verifique os logs:

1. Vá em **Deployments** → Último deploy
2. Veja os logs em tempo real
3. Deve aparecer:
   ```
   🚀 Servidor WhatsApp Web.js rodando em http://localhost:5001
   📱 Client ID: ylada_bot_5001
   ```

Se aparecer erro, verifique:
- ✅ Build Command executou `npm install` com sucesso
- ✅ Start Command está correto
- ✅ Variável PORT está configurada
- ✅ Dependências foram instaladas (node_modules existe)

---

## ⚠️ PROBLEMAS COMUNS

### **Erro: "Cannot find module 'whatsapp-web.js'"**
**Solução:** Build Command não executou `npm install`. Adicione manualmente.

### **Erro: "Port already in use"**
**Solução:** Outro serviço está usando a porta. Verifique variável PORT.

### **Erro: "Command not found: node"**
**Solução:** Railway não detectou como serviço Node.js. Configure manualmente o Build Command.

---

## 📝 NOTAS

- O arquivo `railway.whatsapp.json` já está configurado corretamente
- Se usar o arquivo de configuração, não precisa configurar Start Command manualmente
- O Railway detecta automaticamente Node.js pelo `package.json`
- Dependências são instaladas automaticamente se `package.json` existir

---

**Última atualização:** 2025-01-27

