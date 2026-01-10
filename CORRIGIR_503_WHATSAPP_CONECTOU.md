# 🔧 Corrigir Erro 503 - WhatsApp Conectou mas Plataforma Não Acessa

## ✅ BOM SINAL!

O WhatsApp **conectou no celular**, isso significa que:
- ✅ A autenticação funcionou
- ✅ O servidor Node.js está rodando
- ✅ A sessão foi salva

**O problema agora é:** O Flask não consegue **comunicar** com o servidor Node.js.

---

## 🔍 DIAGNÓSTICO RÁPIDO

### **Cenário 1: Serviço Node.js não está rodando no Railway**

**Sintomas:**
- WhatsApp conectou no celular
- Plataforma mostra erro 503
- Logs do Railway mostram que o serviço Node.js está parado ou crashando

**Solução:**
1. No Railway, vá no serviço WhatsApp (ex: `whatsapp-server-2`)
2. Verifique os logs em **Deployments**
3. Se estiver crashando, veja o erro
4. Faça **Redeploy** se necessário

---

### **Cenário 2: Variável WHATSAPP_SERVER_URL não configurada**

**Sintomas:**
- Serviço Node.js está rodando
- Mas Flask não sabe onde ele está

**Solução:**

#### **PASSO 1: Obter URL do Serviço WhatsApp**

1. No Railway, clique no serviço **WhatsApp** (ex: `whatsapp-server-2`)
2. Vá em **Settings** → **Networking**
3. Procure por **"Public Domain"** ou **"Generate Domain"**
4. **Copie a URL completa** (ex: `https://whatsapp-server-2-production.up.railway.app`)

**OU** use comunicação interna (mais rápido):
- Nome do serviço: `whatsapp-server-2` (ou o nome exato do seu serviço)
- URL interna: `http://whatsapp-server-2:5001`

#### **PASSO 2: Configurar no Serviço Flask**

1. No Railway, clique no serviço **Flask** (ex: `ylada-bot`)
2. Vá em **Variables**
3. Procure por `WHATSAPP_SERVER_URL`
4. Se **não existir**, clique em **+ New Variable**
5. Se **existir**, clique em **Edit**

6. Configure:
   - **Nome:** `WHATSAPP_SERVER_URL`
   - **Valor:** Cole a URL que você copiou
     - **Opção A (URL pública):** `https://whatsapp-server-2-production.up.railway.app`
     - **Opção B (Comunicação interna - RECOMENDADO):** `http://whatsapp-server-2:5001`
       - ⚠️ **IMPORTANTE:** Use o **nome exato** do serviço no Railway!

7. Clique em **Save**

#### **PASSO 3: Aguardar Redeploy**

- O Railway vai fazer redeploy automaticamente
- Aguarde 1-2 minutos
- Verifique os logs do Flask

---

### **Cenário 3: Nome do Serviço Incorreto**

**Sintomas:**
- Variável configurada, mas ainda erro 503
- URL interna não funciona

**Solução:**

1. **Verifique o nome EXATO do serviço:**
   - No Railway, veja o nome do serviço WhatsApp
   - Pode ser: `whatsapp-server-2`, `whatsapp-server`, `whatsapp`, etc.
   - **Use o nome EXATO** (case-sensitive!)

2. **Atualize a variável:**
   ```bash
   WHATSAPP_SERVER_URL=http://NOME-EXATO-DO-SERVICO:5001
   ```
   
   Exemplo:
   ```bash
   WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001
   ```

---

## 🧪 TESTE RÁPIDO

Após configurar, teste:

1. **Acesse a plataforma**
2. **Vá em Conversas** ou **Conectar WhatsApp**
3. **Deve funcionar agora!**

Se ainda der erro 503:
- Verifique os logs do Flask no Railway
- Procure por mensagens de erro sobre conexão
- Verifique se o nome do serviço está correto

---

## 📋 CHECKLIST

- [ ] Serviço WhatsApp está rodando no Railway (verifique logs)
- [ ] Obteve a URL do serviço WhatsApp (pública ou nome interno)
- [ ] Configurou `WHATSAPP_SERVER_URL` no serviço Flask
- [ ] Usou o nome EXATO do serviço (se usar URL interna)
- [ ] Aguardou redeploy completar
- [ ] Testou novamente na plataforma

---

## 💡 DICA: Usar Comunicação Interna

**Recomendado:** Use comunicação interna (mais rápido e não conta no tráfego):

```bash
WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001
```

**Vantagens:**
- ✅ Mais rápido (comunicação interna)
- ✅ Não conta no tráfego público
- ✅ Mais seguro
- ✅ Não precisa de domínio público

**Requisitos:**
- ⚠️ Serviços devem estar no **mesmo projeto** Railway
- ⚠️ Use o **nome exato** do serviço

---

## 🔍 VERIFICAÇÃO FINAL

Após configurar, os logs do Flask devem mostrar:

```
[✓] Servidor WhatsApp está rodando em http://whatsapp-server-2:5001
```

**NÃO deve aparecer:**
- ❌ `Servidor WhatsApp não está acessível`
- ❌ `ConnectionError`
- ❌ `503`

---

**Última atualização:** 2025-01-27

