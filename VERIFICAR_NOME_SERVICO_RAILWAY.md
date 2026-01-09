# 🔍 Verificar Nome do Serviço no Railway

## ⚠️ PROBLEMA

O Flask está tentando acessar `http://whatsapp-server-2:5001`, mas não consegue se conectar.

**Possíveis causas:**
1. O nome do serviço no Railway não é `whatsapp-server-2`
2. A comunicação interna não está funcionando
3. Precisa usar URL pública

---

## 🔍 COMO VERIFICAR O NOME DO SERVIÇO

### **Passo 1: Verificar Nome do Serviço**

1. No Railway, acesse seu projeto
2. Veja a lista de serviços
3. **Procure pelo serviço Node.js** (WhatsApp)
4. **Copie o nome exato** do serviço

**Exemplos de nomes possíveis:**
- `whatsapp-server-2`
- `whatsapp-server`
- `whatsapp`
- `node-whatsapp`
- Outro nome que você deu

---

## ✅ SOLUÇÃO: USAR URL PÚBLICA

Se a comunicação interna não funcionar, use a URL pública:

### **Passo 1: Gerar Domínio Público**

1. No Railway, clique no serviço Node.js (WhatsApp)
2. Vá em **Settings** → **Networking**
3. Clique em **"Generate Domain"** (se ainda não tiver)
4. **Copie a URL gerada** (ex: `https://whatsapp-server-2-production.up.railway.app`)

### **Passo 2: Configurar no Flask**

1. No Railway, clique no serviço **ylada-bot** (Flask)
2. Vá em **Variables**
3. Procure por `WHATSAPP_SERVER_URL`
4. Se existir, clique em **Edit**
5. Se não existir, clique em **+ New Variable**

6. Configure:
   - **Nome:** `WHATSAPP_SERVER_URL`
   - **Valor:** Cole a URL pública que você copiou
     - Exemplo: `https://whatsapp-server-2-production.up.railway.app`

7. Clique em **Save**

---

## 🔄 ALTERNATIVA: CORRIGIR NOME DO SERVIÇO

Se quiser usar comunicação interna, verifique o nome:

### **Passo 1: Verificar Nome Exato**

1. No Railway, veja o nome do serviço Node.js
2. Anote o nome **exatamente como aparece**

### **Passo 2: Atualizar Variável**

1. No serviço `ylada-bot` → **Variables**
2. Configure:
   ```bash
   WHATSAPP_SERVER_URL=http://NOME-EXATO-DO-SERVICO:5001
   ```
   
   **Exemplo:**
   - Se o serviço se chama `whatsapp-server` → `http://whatsapp-server:5001`
   - Se o serviço se chama `whatsapp` → `http://whatsapp:5001`

---

## 🧪 TESTAR

Após configurar:

1. Aguarde 1-2 minutos (redeploy automático)
2. Recarregue a página do QR code
3. Deve funcionar agora! ✅

---

## 📋 CHECKLIST

- [ ] Nome do serviço Node.js verificado no Railway
- [ ] URL pública gerada (ou nome do serviço confirmado)
- [ ] Variável `WHATSAPP_SERVER_URL` configurada no serviço `ylada-bot`
- [ ] Valor salvo corretamente
- [ ] Aguardei redeploy
- [ ] Testei novamente

---

## 💡 RECOMENDAÇÃO

**Use URL pública** para garantir que funcione:
- ✅ Mais confiável
- ✅ Funciona sempre
- ✅ Fácil de debugar

**Comunicação interna** só funciona se:
- ⚠️ Nome do serviço está exato
- ⚠️ Serviços estão no mesmo projeto Railway
- ⚠️ Railway suporta comunicação interna (pode variar)

---

**Última atualização:** 27/01/2025

