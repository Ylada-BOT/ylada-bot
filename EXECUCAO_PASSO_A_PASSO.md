# 🚀 Execução Passo a Passo - Plataforma SaaS

## 📋 DOCUMENTO DE EXECUÇÃO

Este documento contém os passos práticos para desenvolver a plataforma SaaS completa.

---

## 🎯 ORDEM DE EXECUÇÃO

### **ETAPA 1: Sistema de Tenants** (3-4 dias)

#### Passo 1.1: Criar APIs de Tenants
**Arquivo:** `web/api/tenants.py`

```python
from flask import Blueprint, request, jsonify
from src.database.db import SessionLocal
from src.models.tenant import Tenant
from src.models.user import User

bp = Blueprint('tenants', __name__, url_prefix='/api/tenants')

@bp.route('', methods=['POST'])
def create_tenant():
    """Cria novo tenant"""
    # Implementar
    
@bp.route('', methods=['GET'])
def list_tenants():
    """Lista tenants do usuário"""
    # Implementar
    
@bp.route('/<int:tenant_id>', methods=['GET'])
def get_tenant(tenant_id):
    """Obtém detalhes do tenant"""
    # Implementar
```

**Checklist:**
- [ ] Criar arquivo `web/api/tenants.py`
- [ ] Implementar POST /api/tenants (criar)
- [ ] Implementar GET /api/tenants (listar)
- [ ] Implementar GET /api/tenants/:id (detalhes)
- [ ] Implementar PUT /api/tenants/:id (editar)
- [ ] Implementar DELETE /api/tenants/:id (deletar)
- [ ] Registrar blueprint no `web/app.py`

---

#### Passo 1.2: Criar Interface de Tenants
**Arquivo:** `web/templates/tenants/list.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Meus Clientes - BOT YLADA</title>
</head>
<body>
    <h1>Meus Clientes</h1>
    <button onclick="createTenant()">+ Novo Cliente</button>
    
    <div id="tenants-list">
        <!-- Lista de tenants -->
    </div>
</body>
</html>
```

**Checklist:**
- [ ] Criar `web/templates/tenants/list.html`
- [ ] Criar `web/templates/tenants/create.html`
- [ ] Criar `web/templates/tenants/edit.html`
- [ ] Adicionar rotas no `web/app.py`
- [ ] Testar criação de tenant
- [ ] Testar listagem de tenants

---

#### Passo 1.3: Dashboard por Tenant
**Arquivo:** `web/templates/tenants/dashboard.html`

**Checklist:**
- [ ] Criar dashboard isolado por tenant
- [ ] Mostrar instâncias do tenant
- [ ] Mostrar métricas do tenant
- [ ] Adicionar rota `/tenants/<id>/dashboard`

---

### **ETAPA 2: Sistema de Instâncias** (4-5 dias)

#### Passo 2.1: Criar APIs de Instâncias
**Arquivo:** `web/api/instances.py`

**Checklist:**
- [ ] Criar arquivo `web/api/instances.py`
- [ ] Implementar POST /api/instances (criar)
- [ ] Implementar GET /api/instances (listar por tenant)
- [ ] Implementar GET /api/instances/:id (detalhes)
- [ ] Implementar PUT /api/instances/:id (editar)
- [ ] Implementar DELETE /api/instances/:id (deletar)
- [ ] Registrar blueprint no `web/app.py`

---

#### Passo 2.2: Integrar WhatsApp por Instância
**Arquivo:** Modificar `src/whatsapp_webjs_handler.py`

**Checklist:**
- [ ] Modificar para suportar múltiplas instâncias
- [ ] Cada instância tem seu próprio servidor Node.js
- [ ] Cada instância tem sua própria sessão
- [ ] Porta dinâmica por instância (5001, 5002, 5003...)

---

#### Passo 2.3: Interface de Instâncias
**Arquivo:** `web/templates/instances/list.html`

**Checklist:**
- [ ] Criar `web/templates/instances/list.html`
- [ ] Criar `web/templates/instances/create.html`
- [ ] Criar `web/templates/instances/connect.html` (QR Code)
- [ ] Adicionar rotas no `web/app.py`
- [ ] Testar criação de instância
- [ ] Testar conexão WhatsApp por instância

---

### **ETAPA 3: Interface Moderna** (3-4 dias)

#### Passo 3.1: Redesign do Dashboard
**Arquivo:** `web/templates/dashboard.html`

**Checklist:**
- [ ] Criar menu lateral (sidebar)
- [ ] Criar header fixo
- [ ] Redesenhar cards
- [ ] Adicionar cores e estilos modernos
- [ ] Tornar responsivo (mobile)

---

#### Passo 3.2: CSS Moderno
**Arquivo:** `web/static/css/main.css`

**Checklist:**
- [ ] Criar design system (cores, tipografia)
- [ ] Componentes reutilizáveis (cards, buttons, forms)
- [ ] Animações e transições
- [ ] Responsive design

---

### **ETAPA 4: Marketplace** (2-3 semanas)

#### Passo 4.1: Modelo de Templates
**Arquivo:** `src/models/automation_template.py`

**Checklist:**
- [ ] Criar modelo `AutomationTemplate`
- [ ] Campos: name, description, category, niche, flow_data
- [ ] Criar migração do banco
- [ ] Testar criação de template

---

#### Passo 4.2: Interface de Marketplace
**Arquivo:** `web/templates/marketplace/list.html`

**Checklist:**
- [ ] Criar página de marketplace
- [ ] Listar templates disponíveis
- [ ] Filtrar por categoria/nicho
- [ ] Preview do template
- [ ] Botão "Usar este template"

---

#### Passo 4.3: Sistema de Instalação
**Arquivo:** `src/services/template_installer.py`

**Checklist:**
- [ ] Criar serviço de instalação
- [ ] Copiar template para tenant
- [ ] Permitir personalização
- [ ] Ativar como fluxo

---

#### Passo 4.4: Criar Templates Iniciais
**Arquivos:** `data/templates/*.json`

**Checklist:**
- [ ] Template Distribuidores
- [ ] Template E-commerce
- [ ] Template Serviços
- [ ] Template Atendimento
- [ ] Template Captação de Leads

---

## 📝 CHECKLIST GERAL

### **Semana 1-2: Base**
- [ ] Sistema de Tenants completo
- [ ] Sistema de Instâncias completo
- [ ] Interface moderna básica

### **Semana 3-4: Marketplace**
- [ ] Modelo de Templates
- [ ] Interface de Marketplace
- [ ] Sistema de Instalação
- [ ] 5 Templates criados

### **Semana 5: Testes e Ajustes**
- [ ] Testar tudo
- [ ] Corrigir bugs
- [ ] Melhorar UX
- [ ] Documentação

---

## 🛠️ COMANDOS ÚTEIS

### **Criar Migração do Banco:**
```bash
# Se usar Alembic
alembic revision --autogenerate -m "Add tenants and instances"
alembic upgrade head
```

### **Iniciar Servidor:**
```bash
python web/app.py
```

### **Testar APIs:**
```bash
# Criar tenant
curl -X POST http://localhost:5002/api/tenants \
  -H "Content-Type: application/json" \
  -d '{"name": "Meu Cliente", "user_id": 1}'

# Listar tenants
curl http://localhost:5002/api/tenants
```

---

## 🎯 PRÓXIMA AÇÃO

**Começar pela ETAPA 1 - Passo 1.1: Criar APIs de Tenants**

Quer que eu comece criando o arquivo `web/api/tenants.py` agora?

---

**Última atualização:** 13/12/2024

