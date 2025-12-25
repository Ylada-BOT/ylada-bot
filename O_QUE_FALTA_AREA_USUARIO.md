# 📋 O que Falta na Área do Usuário (Tenant)

## ✅ O QUE JÁ EXISTE

### **Rotas Criadas:**
- ✅ `/tenant/dashboard` - Dashboard do tenant
- ✅ `/tenant/flows` - Lista de fluxos
- ✅ `/tenant/flows/new` - Criar fluxo
- ✅ `/tenant/notifications` - Notificações
- ✅ `/tenant/leads` - Leads
- ✅ `/tenant/conversations` - Conversas
- ✅ `/tenant/instances` - Bots
- ✅ `/tenant/qr` - Conectar WhatsApp

### **Templates Criados:**
- ✅ `base_tenant.html` - Base com sidebar (sem Administração)
- ✅ `tenant/dashboard.html` - Dashboard do tenant

---

## ❌ O QUE FALTA

### **1. Templates Faltando (CRÍTICO)**

#### **Templates que não existem:**
- ❌ `tenant/flows/list.html` - Lista de fluxos do tenant
- ❌ `tenant/flows/new.html` - Criar fluxo do tenant
- ❌ `tenant/notifications/list.html` - Notificações do tenant
- ❌ `tenant/leads/list.html` - Leads do tenant
- ❌ `tenant/conversations/list.html` - Conversas do tenant
- ❌ `tenant/instances/list.html` - Bots do tenant
- ❌ `tenant/qr.html` - Conectar WhatsApp (tenant)

**Status:** As rotas existem, mas os templates não. Ao acessar, dá erro 404.

---

### **2. Filtrar Dados por Tenant (CRÍTICO - SEGURANÇA)**

#### **Problema:**
As APIs **NÃO estão filtrando** por `tenant_id`. Isso significa:
- ❌ Tenants podem ver dados de outros tenants
- ❌ Falta de segurança multi-tenant
- ❌ Dados não isolados

#### **APIs que precisam filtrar:**
- ❌ `/api/instances` - Deve mostrar apenas bots do tenant atual
- ❌ `/api/flows` - Deve mostrar apenas fluxos do tenant atual
- ❌ `/api/leads` - Deve mostrar apenas leads do tenant atual
- ❌ `/api/conversations` - Deve mostrar apenas conversas do tenant atual
- ❌ `/api/notifications` - Deve mostrar apenas notificações do tenant atual

#### **O que fazer:**
1. Obter `tenant_id` do usuário atual
2. Filtrar todas as queries por `tenant_id`
3. Admin vê tudo, tenant vê só seus dados

---

### **3. Obter Tenant do Usuário**

#### **Problema:**
Não há função para obter o `tenant_id` do usuário atual.

#### **Solução:**
Criar função `get_current_tenant_id()` que:
- Busca o tenant do usuário logado
- Retorna o `tenant_id`
- Usa nas APIs para filtrar

---

## 🎯 PRIORIDADES

### **PRIORIDADE 1: Segurança (CRÍTICO)**
1. ✅ Filtrar dados por `tenant_id` nas APIs
2. ✅ Criar função `get_current_tenant_id()`
3. ✅ Testar que tenants não veem dados de outros

### **PRIORIDADE 2: Templates (IMPORTANTE)**
1. ✅ Criar templates faltantes para tenant
2. ✅ Usar `base_tenant.html` em todos
3. ✅ Garantir que todas as rotas funcionam

---

## 📝 RESUMO

### **O que falta:**
1. ❌ **7 templates** para área tenant
2. ❌ **Filtro por tenant_id** em todas as APIs (segurança)
3. ❌ **Função para obter tenant do usuário**

### **Impacto:**
- 🔴 **Segurança:** Tenants podem ver dados de outros
- 🔴 **Funcionalidade:** Rotas retornam 404 (templates faltando)
- 🟡 **UX:** Interface incompleta

---

## ✅ PRÓXIMOS PASSOS SUGERIDOS

### **Opção 1: Segurança Primeiro (Recomendado)**
1. Implementar filtro por `tenant_id` nas APIs
2. Criar função `get_current_tenant_id()`
3. Testar isolamento de dados

### **Opção 2: Templates Primeiro**
1. Criar todos os templates faltantes
2. Garantir que rotas funcionam
3. Depois implementar filtros

---

**Última atualização:** 25/12/2024

