# 🔐 Separação: Área Administrativa vs Área Tenant

## ✅ IMPLEMENTAÇÃO

### **Estrutura Criada:**

1. **Área Administrativa** (`/admin/*`)
   - Apenas usuários com role `admin`
   - Gerenciar tenants, usuários, configurações
   - Sidebar: `base.html` (com seção Administração)

2. **Área Tenant** (`/tenant/*`)
   - Usuários normais (não admin)
   - Ver apenas seus próprios dados
   - Sidebar: `base_tenant.html` (sem seção Administração)

---

## 📋 ROTAS CRIADAS

### **Área Administrativa:**
- `/admin` - Dashboard administrativo
- `/admin/tenants` - Lista de tenants
- `/admin/tenants/new` - Criar tenant
- `/admin/tenants/<id>` - Detalhes do tenant
- `/admin/users` - Gerenciar usuários (a criar)
- `/admin/settings` - Configurações (a criar)

### **Área Tenant:**
- `/tenant/dashboard` - Dashboard do tenant
- `/tenant/conversations` - Conversas do tenant
- `/tenant/leads` - Leads do tenant
- `/tenant/flows` - Fluxos do tenant
- `/tenant/notifications` - Notificações do tenant
- `/tenant/instances` - Bots do tenant
- `/tenant/qr` - Conectar WhatsApp do tenant

---

## 🔒 DECORATORS CRIADOS

### **`@require_admin`**
- Exige que o usuário seja admin
- Redireciona se não for admin

### **`@require_tenant`**
- Exige que o usuário NÃO seja admin
- Redireciona admin para área administrativa

---

## 📁 ARQUIVOS CRIADOS

1. **`web/templates/base_tenant.html`**
   - Sidebar para tenants (sem Administração)
   - Navegação focada no uso do bot

2. **`web/templates/base.html`** (atualizado)
   - Sidebar para admins
   - Inclui seção Administração

---

## 🎯 PRÓXIMOS PASSOS

### **1. Criar Templates Admin (2-3h)**
- [ ] `web/templates/admin/dashboard.html`
- [ ] `web/templates/admin/tenants/list.html`
- [ ] `web/templates/admin/tenants/create.html`
- [ ] `web/templates/admin/tenants/dashboard.html`

### **2. Criar Templates Tenant (3-4h)**
- [ ] `web/templates/tenant/dashboard.html`
- [ ] `web/templates/tenant/conversations/list.html`
- [ ] `web/templates/tenant/leads/list.html`
- [ ] `web/templates/tenant/flows/list.html`
- [ ] `web/templates/tenant/notifications/list.html`
- [ ] `web/templates/tenant/instances/list.html`
- [ ] `web/templates/tenant/qr.html`

### **3. Filtrar Dados por Tenant (Importante!)**
- [ ] APIs devem filtrar por `tenant_id` do usuário
- [ ] Tenants só veem seus próprios dados
- [ ] Admins veem tudo

---

## 🔄 COMO FUNCIONA

### **Login:**
1. Usuário faz login
2. Sistema verifica `user_role`
3. Redireciona:
   - `admin` → `/admin`
   - `user` → `/tenant/dashboard`

### **Navegação:**
- **Admin:** Vê sidebar com Administração
- **Tenant:** Vê sidebar sem Administração

### **Acesso:**
- **Admin:** Pode acessar `/admin/*` e ver tudo
- **Tenant:** Só pode acessar `/tenant/*` e ver seus dados

---

## ⚠️ IMPORTANTE

### **Filtrar Dados por Tenant:**
Todas as APIs devem verificar:
```python
# No tenant, só mostra dados do tenant dele
tenant_id = session.get('tenant_id')  # ou do primeiro tenant do usuário
# Filtrar queries por tenant_id
```

### **Admins veem tudo:**
```python
if user_role == 'admin':
    # Mostra todos os dados
else:
    # Filtra por tenant_id
```

---

**Última atualização:** 23/12/2024





