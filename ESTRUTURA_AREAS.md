# 🏗️ Estrutura de Áreas - BOT by YLADA

## ✅ CONFIRMAÇÃO DA ESTRUTURA

### **Área Administrativa** (`/admin/*`)
**Para:** Administradores do sistema

**O que faz:**
- ✅ Gerencia **Tenants** (clientes)
- ✅ Gerencia **Usuários**
- ✅ Vê **Configurações** do sistema
- ✅ Vê **estatísticas gerais**
- ✅ Acessa **tudo**

**Sidebar mostra:**
- Principal: Dashboard, Conversas, Leads
- Automação: Fluxos, Notificações
- Sistema: Conectar WhatsApp
- **Administração:** Tenants, Usuários, Configurações ⭐

---

### **Área Tenant** (`/tenant/*`)
**Para:** Clientes (usuários finais)

**O que faz:**
- ✅ Usa seu **próprio bot**
- ✅ Vê apenas **seus dados**
- ✅ Gerencia **seus fluxos**
- ✅ Vê **suas conversas**
- ✅ Vê **seus leads**
- ❌ **NÃO vê** área administrativa

**Sidebar mostra:**
- Principal: Dashboard, Conversas, Leads
- Automação: Fluxos, Notificações
- Configurações: Meus Bots, Conectar WhatsApp
- ❌ **SEM** seção Administração

---

## 🔐 SEGURANÇA

### **Separação de Dados:**

1. **Tenants só veem seus dados:**
   - Suas conversas
   - Seus leads
   - Seus fluxos
   - Seus bots

2. **Admins veem tudo:**
   - Todos os tenants
   - Todos os usuários
   - Estatísticas gerais
   - Configurações do sistema

---

## 📋 ROTAS

### **Admin:**
- `/admin` - Dashboard administrativo
- `/admin/tenants` - Gerenciar tenants
- `/admin/users` - Gerenciar usuários
- `/admin/settings` - Configurações

### **Tenant:**
- `/tenant/dashboard` - Dashboard do tenant
- `/tenant/conversations` - Conversas do tenant
- `/tenant/leads` - Leads do tenant
- `/tenant/flows` - Fluxos do tenant
- `/tenant/instances` - Bots do tenant
- `/tenant/qr` - Conectar WhatsApp

---

## ✅ ESTÁ CORRETO!

A área administrativa (`/admin/tenants`) é onde os **administradores** gerenciam os **tenants** (clientes).

Cada **tenant** (cliente) tem sua própria área (`/tenant/*`) onde usa o bot sem ver dados de outros tenants.

---

**Última atualização:** 23/12/2024





