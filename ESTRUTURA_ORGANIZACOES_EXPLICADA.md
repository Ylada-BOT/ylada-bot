# 🏢 Estrutura: Organizações, Bots e Automações

## 📊 HIERARQUIA COMPLETA

```
👤 CONTA (User)
│   └── Email: joao@empresa.com
│   └── Senha: ****
│
└── 🏢 ORGANIZAÇÃO 1: "Loja ABC"
    │
    ├── 🤖 BOT 1: "Bot Vendas"
    │   ├── 📱 WhatsApp: (11) 99999-1111
    │   ├── 🔄 Automação: "Bem-vindo"
    │   ├── 🔄 Automação: "Cardápio"
    │   └── 🔄 Automação: "Finalizar Pedido"
    │
    ├── 🤖 BOT 2: "Bot Suporte"
    │   ├── 📱 WhatsApp: (11) 99999-2222
    │   ├── 🔄 Automação: "Abertura de Chamado"
    │   └── 🔄 Automação: "FAQ"
    │
    └── 🔄 AUTOMAÇÕES COMPARTILHADAS (da Organização)
        ├── "Promoção Black Friday"
        └── "Envio de Nota Fiscal"

└── 🏢 ORGANIZAÇÃO 2: "Distribuidora XYZ"
    │
    └── 🤖 BOT 1: "Bot Atacado"
        ├── 📱 WhatsApp: (11) 99999-3333
        └── 🔄 Automação: "Cotação de Preços"
```

---

## 🎯 O QUE É CADA COISA?

### **1. 👤 CONTA (User)**
- **O que é:** Pessoa que faz login no sistema
- **Exemplo:** João Silva (joao@empresa.com)
- **Pode ter:** Várias organizações
- **Área:** `/admin/users`

**Exemplo:**
- João Silva tem 2 organizações:
  - "Loja ABC"
  - "Distribuidora XYZ"

---

### **2. 🏢 ORGANIZAÇÃO (Tenant/Organization)**
- **O que é:** Uma empresa/cliente que usa o sistema
- **Exemplo:** "Loja ABC", "Distribuidora XYZ"
- **Pode ter:**
  - ✅ Vários **BOTS** (WhatsApp diferentes)
  - ✅ Várias **AUTOMAÇÕES** (fluxos)
  - ✅ Vários **LEADS** (contatos)
  - ✅ Várias **CONVERSAS**

**Exemplo:**
- Organização "Loja ABC" tem:
  - 2 bots (Vendas e Suporte)
  - 5 automações
  - 100 leads
  - 50 conversas

---

### **3. 🤖 BOT (Instance)**
- **O que é:** Uma instância WhatsApp conectada
- **Exemplo:** "Bot Vendas", "Bot Suporte"
- **Tem:**
  - ✅ 1 número de WhatsApp
  - ✅ Pode usar várias automações da organização
  - ✅ Conversas próprias
  - ✅ Status (conectado/desconectado)

**Exemplo:**
- Bot "Vendas" usa:
  - Automação "Bem-vindo"
  - Automação "Cardápio"
  - Automação "Finalizar Pedido"

---

### **4. 🔄 AUTOMAÇÃO (Flow)**
- **O que é:** Fluxo de automação (respostas automáticas)
- **Exemplo:** "Bem-vindo", "Cardápio", "FAQ"
- **Pertence a:** Uma organização
- **Pode ser usada por:** Vários bots da mesma organização

**Exemplo:**
- Automação "Bem-vindo" pode ser usada por:
  - Bot "Vendas"
  - Bot "Suporte"
  - (Ambos da mesma organização)

---

## 💡 EXEMPLO PRÁTICO COMPLETO

### **Cenário: João tem uma loja**

```
👤 João Silva (CONTA)
│
└── 🏢 Loja ABC (ORGANIZAÇÃO)
    │
    ├── 🤖 Bot Vendas
    │   ├── 📱 WhatsApp: (11) 98765-4321
    │   ├── 🔄 Usa: "Bem-vindo"
    │   ├── 🔄 Usa: "Cardápio"
    │   └── 🔄 Usa: "Finalizar Pedido"
    │
    ├── 🤖 Bot Delivery
    │   ├── 📱 WhatsApp: (11) 98765-4322
    │   ├── 🔄 Usa: "Bem-vindo"
    │   └── 🔄 Usa: "Horário de Entrega"
    │
    └── 🔄 Automações da Organização:
        ├── "Bem-vindo" (usada por ambos bots)
        ├── "Cardápio"
        ├── "Finalizar Pedido"
        └── "Horário de Entrega"
```

---

## ❓ PERGUNTAS FREQUENTES

### **1. Uma organização pode ter várias automações?**
✅ **SIM!** Uma organização pode ter quantas automações quiser.

**Exemplo:**
- Organização "Loja ABC" tem:
  - Automação "Bem-vindo"
  - Automação "Cardápio"
  - Automação "Finalizar Pedido"
  - Automação "Promoção"
  - Automação "FAQ"

---

### **2. Um bot pode usar várias automações?**
✅ **SIM!** Um bot pode usar várias automações da sua organização.

**Exemplo:**
- Bot "Vendas" usa:
  - Automação "Bem-vindo" (quando recebe "oi")
  - Automação "Cardápio" (quando recebe "cardápio")
  - Automação "Finalizar Pedido" (quando recebe "finalizar")

---

### **3. Vários bots podem usar a mesma automação?**
✅ **SIM!** Se os bots forem da mesma organização.

**Exemplo:**
- Bot "Vendas" usa automação "Bem-vindo"
- Bot "Suporte" usa automação "Bem-vindo"
- (Ambos da organização "Loja ABC")

---

### **4. Uma conta pode ter várias organizações?**
✅ **SIM!** Uma pessoa pode ter várias empresas.

**Exemplo:**
- João Silva tem:
  - Organização "Loja ABC"
  - Organização "Distribuidora XYZ"

---

### **5. Uma organização pode ter vários bots?**
✅ **SIM!** Uma organização pode ter vários WhatsApp.

**Exemplo:**
- Organização "Loja ABC" tem:
  - Bot "Vendas" (WhatsApp 1)
  - Bot "Suporte" (WhatsApp 2)
  - Bot "Delivery" (WhatsApp 3)

---

## 🎯 RESUMO

| Nível | O que é | Pode ter |
|-------|---------|----------|
| **👤 CONTA** | Pessoa que faz login | Várias organizações |
| **🏢 ORGANIZAÇÃO** | Empresa/cliente | Vários bots + Várias automações |
| **🤖 BOT** | WhatsApp conectado | Várias automações (da organização) |
| **🔄 AUTOMAÇÃO** | Fluxo de respostas | Usada por vários bots (da mesma org) |

---

## 📝 EXEMPLO DE USO NO SISTEMA

### **1. João faz login (CONTA)**
- Email: joao@empresa.com
- Vê suas organizações

### **2. Seleciona "Loja ABC" (ORGANIZAÇÃO)**
- Vê os bots da organização
- Vê as automações da organização

### **3. Cria automação "Bem-vindo" (AUTOMAÇÃO)**
- Configura: quando receber "oi" → responder "Olá! Bem-vindo..."
- Fica disponível para todos os bots da organização

### **4. Bot "Vendas" usa a automação**
- Quando alguém manda "oi" no WhatsApp do bot
- A automação "Bem-vindo" é executada
- Responde automaticamente

---

**Última atualização:** 23/12/2024

