# 🔐 Como Acessar a Área Administrativa

## 📍 URL da Área Administrativa

### **URL Principal:**
```
http://localhost:5002/admin
```

---

## 🎯 Rotas Disponíveis

### **1. Dashboard Administrativo**
- **URL:** `/admin`
- **O que faz:** Visão geral do sistema (estatísticas, usuários, organizações)
- **Acesso:** Apenas usuários com role `admin`

### **2. Gerenciar Organizações**
- **URL:** `/admin/tenants`
- **O que faz:** Lista e gerencia todas as organizações
- **Acesso:** Apenas admin

### **3. Criar Organização**
- **URL:** `/admin/tenants/new`
- **O que faz:** Cria uma nova organização
- **Acesso:** Apenas admin

### **4. Ver Organização**
- **URL:** `/admin/tenants/<id>`
- **O que faz:** Dashboard de uma organização específica
- **Acesso:** Apenas admin

### **5. Gerenciar Usuários** (a criar)
- **URL:** `/admin/users`
- **O que faz:** Lista e gerencia usuários do sistema
- **Acesso:** Apenas admin

---

## 🚪 Como Acessar

### **Opção 1: Pela Sidebar**
1. Faça login no sistema
2. No menu lateral, vá em **"Administração"**
3. Clique em **"Organizações"** ou **"Usuários"**

### **Opção 2: URL Direta**
Digite no navegador:
```
http://localhost:5002/admin
```

### **Opção 3: Link no Dashboard**
Se você for admin, o dashboard principal redireciona automaticamente para `/admin`

---

## 🔒 Requisitos de Acesso

### **Autenticação Desabilitada (Desenvolvimento):**
- ✅ Acesso livre a todas as rotas
- ✅ Não precisa fazer login
- ✅ Qualquer um pode acessar `/admin`

### **Autenticação Habilitada (Produção):**
- ✅ Precisa fazer login
- ✅ Precisa ter role `admin` na sessão
- ✅ Se não for admin, redireciona para dashboard principal

---

## 📋 O que Você Vê na Área Administrativa

### **Sidebar (Menu Lateral):**
- **PRINCIPAL:**
  - Dashboard
  - Conversas
  - Leads
- **AUTOMAÇÃO:**
  - Fluxos
  - Notificações
- **SISTEMA:**
  - Conectar WhatsApp
- **ADMINISTRAÇÃO:** ⭐
  - 👥 **Usuários** → Gerencia pessoas que fazem login
  - 🏢 **Organizações** → Gerencia empresas/clientes
  - ⚙️ **Configurações** → Configurações do sistema

---

## 🎯 Diferença: Admin vs Tenant

### **Área Administrativa (`/admin/*`):**
- ✅ Vê **TODAS** as organizações
- ✅ Vê **TODOS** os usuários
- ✅ Gerencia o sistema inteiro
- ✅ Acesso completo

### **Área Tenant (`/tenant/*`):**
- ✅ Vê apenas **SUA** organização
- ✅ Vê apenas **SEUS** dados
- ✅ Não vê área administrativa
- ✅ Acesso limitado

---

## 🔧 Como Habilitar/Desabilitar Autenticação

### **No arquivo `.env` ou variável de ambiente:**
```bash
# Desabilitado (desenvolvimento)
AUTH_REQUIRED=false

# Habilitado (produção)
AUTH_REQUIRED=true
```

### **No código (`web/app.py`):**
```python
AUTH_REQUIRED = os.getenv('AUTH_REQUIRED', 'false').lower() == 'true'
```

---

## 📝 Exemplo de Uso

### **1. Acessar Dashboard Admin:**
```
http://localhost:5002/admin
```

### **2. Ver Todas as Organizações:**
```
http://localhost:5002/admin/tenants
```

### **3. Criar Nova Organização:**
```
http://localhost:5002/admin/tenants/new
```

---

## ⚠️ Importante

- Se a autenticação estiver **desabilitada**, você pode acessar `/admin` diretamente
- Se a autenticação estiver **habilitada**, precisa:
  1. Fazer login
  2. Ter role `admin` na sessão
  3. Se não for admin, será redirecionado

---

**Última atualização:** 23/12/2024





