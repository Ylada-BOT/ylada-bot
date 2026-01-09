# 🔧 Verificar e Corrigir Erro 503 - Servidor WhatsApp

## ⚠️ PROBLEMA

**Erro 503: Servidor WhatsApp não está disponível**

O servidor Node.js do WhatsApp não está rodando ou não está acessível no Railway.

---

## ✅ SOLUÇÃO PASSO A PASSO

### **PASSO 1: Verificar se o Serviço WhatsApp Existe no Railway**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. Veja a lista de serviços

**Procure por um serviço com nome similar a:**
- `whatsapp-server`
- `whatsapp-server-2`
- `whatsapp`
- `node-whatsapp`
- Ou outro nome que você deu

**Se NÃO existir nenhum serviço Node.js:**
- Vá para **PASSO 2** (Criar Serviço)

**Se existir:**
- Vá para **PASSO 3** (Verificar se Está Rodando)

---

### **PASSO 2: Criar Serviço WhatsApp no Railway**

1. No Railway, clique em **"New"** → **"Empty Service"**
2. **Nome:** `whatsapp-server` (ou outro nome de sua escolha)
3. **Settings** → **Deploy**:
   - **Build Command:** `npm install`
   - **Start Command:** `node whatsapp_server.js`
   - **Root Directory:** `/` (raiz do projeto)
4. **Settings** → **Variables**:
   ```bash
   PORT=5001
   NODE_ENV=production
   ```
5. **Settings** → **Networking**:
   - Clique em **"Generate Domain"**
   - **Copie a URL gerada** (ex: `https://whatsapp-server-production.up.railway.app`)
   - Esta URL será usada no próximo passo

---

### **PASSO 3: Verificar se o Serviço Está Rodando**

1. No Railway, selecione o serviço WhatsApp
2. Vá em **Deployments**
3. Veja os logs mais recentes
4. **Deve aparecer:**
   - ✅ `Servidor WhatsApp iniciado na porta 5001`
   - ✅ `Health check disponível em /health`
   - ✅ `Modo: Múltiplos usuários (suporta user_id)`

**Se estiver crashando:**
- Veja os logs para identificar o erro
- Verifique se o Start Command está correto: `node whatsapp_server.js`
- Verifique se o arquivo `whatsapp_server.js` existe no repositório

---

### **PASSO 4: Configurar URL no Serviço Flask**

1. No Railway, selecione o serviço **Flask/Python** (geralmente chamado `ylada-bot` ou similar)
2. Vá em **Settings** → **Variables**
3. Procure por `WHATSAPP_SERVER_URL`
4. **Se existir:**
   - Clique em **Edit**
   - Verifique se a URL está correta
5. **Se não existir:**
   - Clique em **+ New Variable**
   - **Nome:** `WHATSAPP_SERVER_URL`
   - **Valor:** Cole a URL pública do serviço WhatsApp que você copiou no Passo 2
     - Exemplo: `https://whatsapp-server-production.up.railway.app`
     - **IMPORTANTE:** Use a URL completa com `https://`
6. Clique em **Save**

---

### **PASSO 5: Verificar Variável de Ambiente**

No serviço Flask, verifique se estas variáveis estão configuradas:

```bash
# Verifica se está em produção
IS_PRODUCTION=true

# URL do servidor WhatsApp (obrigatório em produção)
WHATSAPP_SERVER_URL=https://whatsapp-server-production.up.railway.app

# Porta padrão (opcional, padrão é 5001)
WHATSAPP_SERVER_PORT=5001
```

---

### **PASSO 6: Aguardar Redeploy**

Após configurar a variável `WHATSAPP_SERVER_URL`:

1. O Railway deve detectar a mudança e fazer redeploy automaticamente
2. Aguarde 2-5 minutos
3. Verifique os logs do serviço Flask para confirmar que está usando a URL correta

---

### **PASSO 7: Testar**

1. Acesse: `https://yladabot.com/qr`
2. **Deve aparecer:**
   - ✅ QR Code (se não estiver conectado)
   - ✅ Status "Conectado" (se já estiver conectado)
   - ❌ **NÃO deve aparecer erro 503**

---

## 🔍 TROUBLESHOOTING

### **Erro 503 ainda aparece após configurar URL**

1. **Verifique se o serviço WhatsApp está rodando:**
   - Railway → Serviço WhatsApp → Deployments → Logs
   - Deve mostrar que o servidor iniciou

2. **Verifique se a URL está correta:**
   - A URL deve começar com `https://`
   - A URL não deve ter porta no final (ex: `:5001`)
   - Exemplo correto: `https://whatsapp-server-production.up.railway.app`
   - Exemplo errado: `https://whatsapp-server-production.up.railway.app:5001`

3. **Teste a URL manualmente:**
   - Abra no navegador: `https://whatsapp-server-production.up.railway.app/health`
   - Deve retornar: `{"status":"ok"}`

4. **Verifique os logs do Flask:**
   - Railway → Serviço Flask → Deployments → Logs
   - Procure por mensagens de erro ao conectar no servidor WhatsApp

---

### **Serviço WhatsApp está crashando**

1. **Verifique os logs:**
   - Railway → Serviço WhatsApp → Deployments → Logs
   - Procure por erros em vermelho

2. **Erros comuns:**
   - **"Cannot find module 'whatsapp-web.js'"**
     - Solução: Adicione `package.json` com dependências
   - **"Port already in use"**
     - Solução: Verifique se há outro processo usando a porta 5001
   - **"SyntaxError"**
     - Solução: Verifique se o arquivo `whatsapp_server.js` está correto

---

### **URL está correta mas ainda não funciona**

1. **Use comunicação interna (se serviços estão no mesmo projeto):**
   ```bash
   WHATSAPP_SERVER_URL=http://whatsapp-server:5001
   ```
   (Substitua `whatsapp-server` pelo nome exato do seu serviço)

2. **Verifique se o serviço WhatsApp tem domínio público:**
   - Railway → Serviço WhatsApp → Settings → Networking
   - Deve ter um domínio gerado

---

## 📋 CHECKLIST

- [ ] Serviço WhatsApp existe no Railway
- [ ] Serviço WhatsApp está rodando (ver logs)
- [ ] URL pública foi gerada no serviço WhatsApp
- [ ] Variável `WHATSAPP_SERVER_URL` está configurada no serviço Flask
- [ ] URL está no formato correto (`https://...`)
- [ ] Aguardou redeploy (2-5 minutos)
- [ ] Testou `/health` no navegador
- [ ] Testou `/qr` na aplicação

---

## 💡 DICA

Se você tem múltiplos serviços WhatsApp (um por porta), cada um precisa:
- Ser um serviço separado no Railway
- Ter sua própria URL pública
- Ser configurado no Flask com a URL correta

Para múltiplas instâncias do mesmo usuário, todas usam o mesmo serviço WhatsApp (porta 5001), mas com `user_id` diferentes.

