# 🔗 Como Obter a URL do Serviço no Railway

## 📍 ONDE ENCONTRAR

### **PASSO 1: Acessar Settings do Serviço**

1. No Railway, clique no serviço **whatsapp-server-2**
2. Vá em **Settings** (ou clique na aba "Settings")

### **PASSO 2: Ir em Networking**

1. Role a página até encontrar a seção **"Networking"** ou **"Domains"**
2. Você verá:
   - **"Public Domain"** ou **"Custom Domain"**
   - Ou um botão **"Generate Domain"**

### **PASSO 3: Ver ou Gerar Domínio**

**Se já tem domínio:**
- Você verá algo como: `https://whatsapp-server-2.railway.app`
- Copie essa URL

**Se não tem domínio:**
1. Clique em **"Generate Domain"** ou **"Add Domain"**
2. O Railway vai gerar uma URL automaticamente
3. Copie a URL gerada

---

## 🔍 ONDE APARECE A URL

A URL geralmente aparece em um destes formatos:

```
https://whatsapp-server-2.railway.app
https://whatsapp-server-2-production.up.railway.app
https://whatsapp-server-2-xxxxx.up.railway.app
```

Onde `xxxxx` é um código único do Railway.

---

## 📋 EXEMPLO VISUAL

```
Settings → Networking
├── Public Domain
│   └── https://whatsapp-server-2.railway.app  ← ESTA É A URL!
└── [Generate Domain] (se não tiver)
```

---

## ✅ DEPOIS DE OBTER A URL

1. **Copie a URL completa** (com `https://`)
2. **No serviço ylada-bot**, vá em **Variables**
3. **Adicione ou atualize:**
   ```bash
   WHATSAPP_SERVER_URL=https://whatsapp-server-2.railway.app
   ```
   (Substitua pela URL real que você copiou)
4. **Salve**
5. **Aguarde redeploy**

---

## 💡 DICA

Se você não conseguir encontrar, tente:

1. **Settings** → **Networking** → **Generate Domain**
2. Ou veja em **Deployments** → Último deploy → pode aparecer a URL nos logs

---

**Última atualização:** 27/01/2025

