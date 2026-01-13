# 🔧 SOLUÇÃO COMPLETA: Erros 429 e 503

## ✅ O QUE FOI CORRIGIDO

### 1. **Erro 429 (Too Many Requests) - RESOLVIDO**
- ❌ **Problema:** `default_limits = ["200 per hour"]` estava bloqueando TODAS as rotas
- ✅ **Solução:** Removido `default_limits` completamente (agora é `[]`)
- ✅ **Solução:** Removido `@rate_limit_status` de `/api/qr` (não precisa, é apenas leitura)
- ✅ **Resultado:** Apenas rotas com decorators específicos têm rate limiting:
  - `/api/whatsapp-status` → 100/min, 5000/hora
  - `/webhook` → 15/min, 800/dia

### 2. **Erro 503 (Service Unavailable) - VERIFICAR**

O erro 503 acontece quando o Flask não consegue conectar com o servidor WhatsApp.

**Possíveis causas:**
1. ❌ Servidor WhatsApp não está rodando no Railway
2. ❌ Nome do serviço WhatsApp está errado
3. ❌ URL de comunicação está incorreta

---

## 🔍 VERIFICAÇÃO EM PRODUÇÃO (Railway)

### **PASSO 1: Verificar se Serviço WhatsApp Existe**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. Veja se há um serviço chamado:
   - `whatsapp-server-2` (ou similar)
   - Deve estar na lista de serviços

**Se NÃO existir:**
- Crie um novo serviço (veja PASSO 2)

**Se existir:**
- Vá para PASSO 3

---

### **PASSO 2: Criar Serviço WhatsApp (se não existir)**

1. No Railway, clique em **"New"** → **"Empty Service"**
2. Nome: `whatsapp-server-2` (ou o nome que você preferir)
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
   - NÃO precisa gerar domínio público
   - O Flask vai usar comunicação interna via nome do serviço

---

### **PASSO 3: Verificar Status do Serviço WhatsApp**

1. No Railway, selecione o serviço WhatsApp
2. Verifique o status:
   - ✅ **"Online"** = Serviço está rodando (OK)
   - ❌ **"Crashed"** = Serviço parou (veja logs)
   - ❌ **"Completed"** = Serviço terminou (não deveria acontecer)

**Se estiver "Crashed" ou "Completed":**
- Veja os logs (aba "Deployments" → "Logs")
- Procure por erros
- Faça redeploy se necessário

---

### **PASSO 4: Verificar Nome do Serviço no Flask**

O Flask precisa saber o nome exato do serviço WhatsApp.

1. No Railway, selecione o serviço **Flask/Python**
2. Vá em **Settings** → **Variables**
3. Verifique se existe:
   - `WHATSAPP_SERVICE_NAME` = nome exato do serviço WhatsApp
   - Exemplo: Se o serviço se chama `whatsapp-server-2`, configure:
     ```bash
     WHATSAPP_SERVICE_NAME=whatsapp-server-2
     ```

**Se não existir:**
- Clique em **"+ New Variable"**
- Nome: `WHATSAPP_SERVICE_NAME`
- Valor: Nome exato do serviço WhatsApp (ex: `whatsapp-server-2`)
- Salve

---

### **PASSO 5: Verificar Logs do Flask**

1. No Railway, selecione o serviço **Flask/Python**
2. Vá em **Deployments** → **Logs**
3. Procure por mensagens quando tentar acessar `/api/qr`:
   - `Buscando QR Code do servidor WhatsApp em http://...`
   - `Tentando acessar: http://...`
   - `Server URL configurada: http://...`

**Se aparecer erro:**
- Copie a mensagem de erro completa
- Verifique se a URL está correta
- Verifique se o nome do serviço está correto

---

## 📋 RESUMO DO QUE FOI FEITO

1. ✅ Removido `default_limits` do rate limiter
2. ✅ Removido `@rate_limit_status` de `/api/qr`
3. ✅ Melhorado tratamento de erro 503 com logs detalhados
4. ✅ Mensagens de erro mais claras

---

## 🎯 PRÓXIMOS PASSOS

1. **Aguarde 1-2 minutos** para o deploy aplicar
2. **Teste novamente** em produção
3. **Se ainda der erro 503:**
   - Verifique se o serviço WhatsApp está rodando (PASSO 3)
   - Verifique o nome do serviço (PASSO 4)
   - Veja os logs do Flask (PASSO 5)

---

## ⚠️ IMPORTANTE

- **Erro 429:** Deve estar resolvido agora (sem rate limiting em `/api/qr`)
- **Erro 503:** Geralmente significa que o servidor WhatsApp não está rodando ou não está acessível
- **Em desenvolvimento:** O servidor WhatsApp deve estar rodando na porta 5001
- **Em produção:** O serviço WhatsApp deve estar online no Railway

---

**Última atualização:** 13/01/2026
