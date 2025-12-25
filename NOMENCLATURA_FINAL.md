# 📝 Nomenclatura Final - Opção 1

## ✅ ESTRUTURA DEFINIDA

### **Hierarquia:**
```
👤 Usuário (User)
├── 🏢 Organização 1 (Tenant)
│   ├── 🤖 Bot 1 (Instance)
│   └── 🤖 Bot 2 (Instance)
└── 🏢 Organização 2 (Tenant)
    └── 🤖 Bot 3 (Instance)
```

---

## 📋 NOMENCLATURA

### **1. Usuários** 👤
- **O que é:** Pessoas que fazem login no sistema
- **Modelo:** `User`
- **Área:** `/admin/users`
- **Pode ter:** Várias organizações

### **2. Organizações** 🏢
- **O que é:** Cada empresa/cliente (tenant)
- **Modelo:** `Tenant`
- **Área:** `/admin/tenants`
- **Pode ter:** Vários bots

### **3. Bots** 🤖
- **O que é:** Instâncias WhatsApp
- **Modelo:** `Instance`
- **Área:** `/instances`
- **Pertence a:** Uma organização

---

## 🎯 ÁREA ADMINISTRATIVA

### **Sidebar:**
- 👤 **Usuários** → Gerencia pessoas
- 🏢 **Organizações** → Gerencia empresas/clientes
- ⚙️ **Configurações** → Configurações do sistema

### **Dashboard Admin:**
- 👤 **Usuários** → Total de pessoas
- 🏢 **Organizações** → Total de empresas
- 🤖 **Bots** → Total de instâncias
- 🔄 **Fluxos** → Total de fluxos

---

## 📁 ARQUIVOS ATUALIZADOS

### **Templates:**
1. ✅ `base.html` - Sidebar atualizada
2. ✅ `admin/dashboard.html` - Cards atualizados
3. ✅ `tenants/list.html` - "Organizações"
4. ✅ `tenants/create.html` - "Criar Organização"
5. ✅ `tenants/dashboard.html` - "Dashboard da Organização"
6. ✅ `instances/list.html` - Referências atualizadas

### **Mantido (código técnico):**
- ✅ Rotas: `/admin/tenants`, `/api/tenants`
- ✅ Variáveis: `tenant_id`, `tenant.name`
- ✅ Modelos: `Tenant`, `User`, `Instance`

---

## 💡 EXEMPLO DE USO

### **Cenário:**
João Silva (👤 Usuário) tem:
- 🏢 Loja ABC (Organização 1)
  - 🤖 Bot Vendas
  - 🤖 Bot Suporte
- 🏢 Distribuidora XYZ (Organização 2)
  - 🤖 Bot Atacado

### **Fluxo:**
1. João faz login (👤 Usuário)
2. Vê suas organizações (🏢)
3. Seleciona uma organização
4. Vê os bots da organização (🤖)
5. Gerencia cada bot

---

## ✅ CONCLUÍDO

A nomenclatura está atualizada na interface:
- **Usuários** = Pessoas
- **Organizações** = Empresas/Clientes (tenants)
- **Bots** = Instâncias WhatsApp

**Última atualização:** 23/12/2024


