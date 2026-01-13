# 📍 COMO ADICIONAR WHATSAPP_SERVICE_NAME NO RAILWAY

## 🎯 OBJETIVO

Adicionar a variável `WHATSAPP_SERVICE_NAME` no serviço Flask (ylada-bot) do Railway.

---

## 📋 PASSO A PASSO (COM IMAGENS)

### **PASSO 1: Acessar o Serviço Flask**

1. Acesse: https://railway.app
2. Selecione seu projeto
3. **Clique no serviço "ylada-bot"** (ou "ylad" - o serviço Flask/Python)
   - É o serviço que tem o domínio `yladabot.com`
   - Deve estar com status "Online" (bolinha verde)

---

### **PASSO 2: Abrir Configurações de Variáveis**

1. Com o serviço "ylada-bot" selecionado, procure por:
   - **Aba "Variables"** (no topo)
   - **Ou "Settings" → "Variables"** (no menu lateral)
   - **Ou clique em "Variables"** na barra superior

2. Você verá uma lista de variáveis como:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - `PORT`
   - `SECRET_KEY`
   - `WHATSAPP_SERVER_URL`
   - etc.

---

### **PASSO 3: Adicionar Nova Variável**

1. Procure por um botão que diz:
   - **"+ New Variable"** (botão azul/roxo)
   - **"+ Add Variable"**
   - **"New"** → **"Variable"**
   - Geralmente fica no canto superior direito da lista de variáveis

2. **Clique nesse botão**

---

### **PASSO 4: Preencher os Campos**

1. **Campo "Key" ou "Name":**
   - Digite exatamente: `WHATSAPP_SERVICE_NAME`
   - (sem espaços, exatamente assim)

2. **Campo "Value" ou "Valor":**
   - Digite o nome exato do serviço WhatsApp
   - Olhe no painel esquerdo do Railway
   - Procure pelo serviço que se chama `whatsapp-server-2`
   - Digite: `whatsapp-server-2`
   - (ou o nome exato que aparecer no seu Railway)

3. **Clique em "Add" ou "Save"**

---

### **PASSO 5: Verificar se Foi Adicionado**

1. Volte para a lista de variáveis
2. Procure por `WHATSAPP_SERVICE_NAME` na lista
3. Deve aparecer algo como:
   ```
   WHATSAPP_SERVICE_NAME = whatsapp-server-2
   ```

---

## 🔍 ONDE ENCONTRAR O NOME DO SERVIÇO WHATSAPP

1. No painel esquerdo do Railway (lista de serviços)
2. Procure pelo serviço que tem:
   - Nome: `whatsapp-server-2` (ou similar)
   - Status: "Online" (bolinha verde)
   - É o serviço Node.js (não o Flask)

3. **O nome que aparece ali é o que você deve usar!**
   - Exemplo: Se aparece `whatsapp-server-2`, use `whatsapp-server-2`
   - Exemplo: Se aparece `whatsapp`, use `whatsapp`

---

## ⚠️ IMPORTANTE

- **NÃO** adicione no serviço WhatsApp
- **SIM**, adicione no serviço Flask (ylada-bot)
- O nome deve ser **exatamente igual** ao nome do serviço WhatsApp
- Sem espaços, sem caracteres especiais
- Após adicionar, aguarde 1-2 minutos para o deploy aplicar

---

## 📸 ONDE ESTÁ NO RAILWAY

```
Railway Dashboard
├── [Painel Esquerdo] Lista de Serviços
│   ├── whatsapp-server-2 ← Nome do serviço WhatsApp (use este nome!)
│   └── ylada-bot ← Clique AQUI para adicionar a variável
│
└── [Painel Direito] Quando clicar em ylada-bot:
    ├── Aba "Variables" ← Clique AQUI
    │   ├── Lista de variáveis existentes
    │   └── Botão "+ New Variable" ← Clique AQUI
    │       ├── Key: WHATSAPP_SERVICE_NAME
    │       └── Value: whatsapp-server-2 (nome do serviço)
```

---

## ✅ DEPOIS DE ADICIONAR

1. Aguarde 1-2 minutos
2. O Railway vai fazer redeploy automaticamente
3. Teste novamente em `yladabot.com/qr`
4. O erro não deve mais aparecer

---

## 🆘 SE NÃO ENCONTRAR

**Opção 1: Procurar por "Variables"**
- Use Ctrl+F (ou Cmd+F no Mac)
- Digite "Variables"
- Deve aparecer a aba ou seção

**Opção 2: Procurar por "Settings"**
- Clique em "Settings" no menu
- Procure por "Variables" ou "Environment Variables"

**Opção 3: Menu de três pontos**
- Procure por um ícone de três pontos (`...`) ao lado do serviço
- Clique nele
- Procure por "Variables" ou "Environment"

---

**Última atualização:** 13/01/2026
