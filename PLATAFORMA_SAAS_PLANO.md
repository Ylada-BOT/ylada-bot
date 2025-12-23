# 🚀 Plano: Plataforma SaaS Multi-Tenant (Tipo ManyChat)

## 🎯 Visão Geral

Transformar o BOT YLADA em uma **plataforma SaaS** onde:
- ✅ Cada cliente (tenant) tem seu próprio bot/WhatsApp
- ✅ Cada cliente pode ter múltiplas instâncias (bots)
- ✅ Marketplace de automações prontas por nicho
- ✅ Sistema de assinaturas/planos
- ✅ Vender automações prontas (distribuidores, e-commerce, etc)

---

## 📊 O QUE JÁ TEMOS ✅

### Estrutura Multi-Tenant:
- ✅ Modelo `Tenant` - Cada cliente
- ✅ Modelo `Instance` - Cada bot/WhatsApp
- ✅ Modelo `User` - Dono do tenant
- ✅ Modelo `Subscription` - Assinaturas
- ✅ Modelo `Plan` - Planos de preço
- ✅ Sistema de fluxos por tenant
- ✅ Leads, conversas, notificações isolados por tenant

### O que falta implementar:
- ❌ Interface de gerenciamento de tenants
- ❌ Marketplace de automações
- ❌ Sistema de templates por nicho
- ❌ Interface para criar/gerenciar instâncias
- ❌ Dashboard por tenant
- ❌ Sistema de pagamento

---

## 🎯 FASE 1: Base da Plataforma (1-2 semanas)

### 1.1 Sistema de Tenants e Instâncias ⭐ **CRÍTICO**

**O que fazer:**
- [ ] Interface para criar novo tenant
- [ ] Interface para criar nova instância (bot)
- [ ] Cada instância = 1 WhatsApp conectado
- [ ] Gerenciar múltiplas instâncias por tenant
- [ ] Dashboard isolado por tenant
- [ ] Trocar entre instâncias no dashboard

**Arquivos a criar:**
- `web/templates/tenants/list.html` - Lista de tenants (admin)
- `web/templates/tenants/create.html` - Criar tenant
- `web/templates/instances/list.html` - Lista de instâncias do tenant
- `web/templates/instances/create.html` - Criar nova instância
- `web/api/tenants.py` - APIs de tenants
- `web/api/instances.py` - APIs de instâncias

**Resultado:** Cada cliente pode ter seu próprio bot isolado!

---

### 1.2 Marketplace de Automações ⭐ **DIFERENCIAL**

**O que fazer:**
- [ ] Modelo `AutomationTemplate` no banco
  - Nome, descrição, categoria (vendas, atendimento, etc)
  - Nicho (distribuidores, e-commerce, serviços, etc)
  - Fluxo JSON completo
  - Preview/imagem
  - Preço (se for pago)
- [ ] Interface de marketplace
  - Listar templates disponíveis
  - Filtrar por nicho/categoria
  - Preview do fluxo
  - Botão "Usar este template"
- [ ] Sistema de instalação
  - Copiar template para tenant
  - Personalizar antes de ativar
  - Ativar template

**Arquivos a criar:**
- `src/models/automation_template.py` - Modelo de template
- `web/templates/marketplace/list.html` - Marketplace
- `web/templates/marketplace/detail.html` - Detalhes do template
- `web/api/marketplace.py` - APIs do marketplace

**Templates iniciais a criar:**
- 📦 **Distribuidores** - Vendas B2B, catálogo, pedidos
- 🛒 **E-commerce** - Vendas online, checkout, rastreamento
- 🏥 **Serviços** - Agendamentos, confirmações, lembretes
- 🎓 **Educação** - Matrículas, informações, suporte
- 🍕 **Delivery** - Pedidos, cardápio, rastreamento

**Resultado:** Clientes podem escolher automações prontas por nicho!

---

### 1.3 Sistema de Planos e Assinaturas

**O que fazer:**
- [ ] Interface para gerenciar planos
- [ ] Limites por plano:
  - Número de instâncias
  - Número de fluxos
  - Mensagens por mês
  - Templates disponíveis
- [ ] Sistema de trial (período de teste)
- [ ] Bloquear funcionalidades se exceder limite
- [ ] Dashboard de uso (mensagens, instâncias, etc)

**Arquivos a criar:**
- `web/templates/plans/list.html` - Planos disponíveis
- `web/templates/subscriptions/manage.html` - Gerenciar assinatura
- `web/api/subscriptions.py` - APIs de assinatura

**Resultado:** Sistema de monetização funcionando!

---

## 🎯 FASE 2: Funcionalidades Avançadas (2-3 semanas)

### 2.1 IA Treinada por Nicho ⭐ **DIFERENCIAL**

**O que fazer:**
- [ ] System prompts pré-configurados por nicho
  - Distribuidores: "Você é um vendedor B2B especializado em..."
  - E-commerce: "Você é um atendente de e-commerce..."
  - Serviços: "Você é um assistente de agendamento..."
- [ ] Treinar IA com contexto do negócio
  - Upload de catálogo de produtos
  - Informações da empresa
  - Perguntas frequentes
- [ ] Fine-tuning por tenant (opcional, futuro)

**Arquivos a criar:**
- `src/ai/prompt_templates.py` - Templates de prompts por nicho
- `web/templates/ai/train.html` - Treinar IA
- `web/api/ai/train.py` - APIs de treinamento

**Resultado:** Cada bot tem IA especializada no nicho!

---

### 2.2 Editor Visual de Fluxos

**O que fazer:**
- [ ] Interface drag & drop para criar fluxos
- [ ] Visualizar fluxo como diagrama
- [ ] Adicionar/remover steps visualmente
- [ ] Testar fluxo antes de ativar
- [ ] Exportar/importar fluxos

**Resultado:** Criar automações fica muito mais fácil!

---

### 2.3 Analytics e Relatórios por Tenant

**O que fazer:**
- [ ] Dashboard de métricas por tenant
  - Mensagens enviadas/recebidas
  - Conversões (leads, vendas)
  - Fluxos mais usados
  - Horários de pico
- [ ] Relatórios exportáveis
- [ ] Comparar performance entre instâncias

**Resultado:** Clientes veem resultados do investimento!

---

## 🎯 FASE 3: Monetização e Escala (2-3 semanas)

### 3.1 Sistema de Pagamento

**O que fazer:**
- [ ] Integração com gateway (Stripe, Mercado Pago, Asaas)
- [ ] Checkout para assinaturas
- [ ] Renovação automática
- [ ] Upgrade/downgrade de plano
- [ ] Faturas e recibos

**Resultado:** Recebimentos automáticos!

---

### 3.2 White Label (Opcional)

**O que fazer:**
- [ ] Personalização de marca por tenant
- [ ] Domínio próprio (subdomain)
- [ ] Logo e cores customizadas
- [ ] Email personalizado

**Resultado:** Clientes podem usar sua própria marca!

---

### 3.3 API Pública

**O que fazer:**
- [ ] API REST completa
- [ ] Webhooks para integrações
- [ ] Documentação (Swagger)
- [ ] SDKs (Python, Node.js)

**Resultado:** Integrações com outros sistemas!

---

## 📋 ESTRUTURA DE BANCO DE DADOS

### Novas Tabelas Necessárias:

```sql
-- Templates de automação (marketplace)
CREATE TABLE automation_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100), -- vendas, atendimento, agendamento
    niche VARCHAR(100), -- distribuidores, e-commerce, serviços
    flow_data JSONB NOT NULL,
    preview_image VARCHAR(500),
    price DECIMAL(10,2) DEFAULT 0,
    is_premium BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Templates instalados por tenant
CREATE TABLE tenant_templates (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    template_id INTEGER REFERENCES automation_templates(id),
    installed_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Configurações de IA por tenant
CREATE TABLE tenant_ai_configs (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    instance_id INTEGER REFERENCES instances(id),
    provider VARCHAR(50), -- openai, anthropic
    model VARCHAR(100),
    system_prompt TEXT,
    context_data JSONB, -- produtos, FAQ, etc
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🎨 INTERFACES NECESSÁRIAS

### Para Admin (Você):
1. **Dashboard Admin**
   - Total de tenants
   - Receita mensal
   - Tenants ativos/inativos
   - Templates mais usados

2. **Gerenciar Templates**
   - Criar/editar templates
   - Definir preço
   - Ativar/desativar
   - Ver estatísticas de uso

3. **Gerenciar Tenants**
   - Listar todos os tenants
   - Ver detalhes de cada um
   - Suspender/ativar
   - Ver uso (mensagens, instâncias)

### Para Cliente (Tenant):
1. **Dashboard do Cliente**
   - Suas instâncias (bots)
   - Métricas do seu negócio
   - Assinatura atual
   - Uso do mês

2. **Gerenciar Instâncias**
   - Criar nova instância (bot)
   - Conectar WhatsApp
   - Ver status de cada bot
   - Configurar IA

3. **Marketplace**
   - Ver templates disponíveis
   - Filtrar por nicho
   - Instalar template
   - Personalizar antes de ativar

4. **Meus Fluxos**
   - Ver fluxos ativos
   - Criar novo fluxo
   - Editar fluxo existente
   - Usar template do marketplace

---

## 🚀 ROADMAP SUGERIDO

### **Semana 1-2: Base**
- [ ] Sistema de tenants e instâncias
- [ ] Dashboard isolado por tenant
- [ ] Criar/gerenciar instâncias

### **Semana 3-4: Marketplace**
- [ ] Modelo de templates
- [ ] Interface de marketplace
- [ ] Criar 5 templates iniciais (distribuidores, e-commerce, etc)
- [ ] Sistema de instalação

### **Semana 5-6: IA e Fluxos**
- [ ] IA treinada por nicho
- [ ] Editor visual de fluxos (básico)
- [ ] Templates de prompts por nicho

### **Semana 7-8: Monetização**
- [ ] Sistema de planos funcionando
- [ ] Integração com pagamento
- [ ] Analytics por tenant

### **Semana 9-10: Polimento**
- [ ] Testes
- [ ] Documentação
- [ ] Onboarding de clientes

---

## 💡 PRÓXIMOS PASSOS IMEDIATOS

### **1. Criar Interface de Tenants** (2-3 dias)
- Página para criar tenant
- Lista de tenants do usuário
- Dashboard por tenant

### **2. Criar Sistema de Instâncias** (2-3 dias)
- Cada tenant pode ter múltiplas instâncias
- Cada instância = 1 WhatsApp
- Conectar WhatsApp por instância

### **3. Criar Marketplace Básico** (3-4 dias)
- Modelo de template
- Interface de marketplace
- Criar 2-3 templates iniciais

---

## ❓ O QUE VOCÊ QUER COMEÇAR?

1. **Sistema de Tenants e Instâncias** - Base da plataforma
2. **Marketplace de Templates** - Diferencial competitivo
3. **IA Treinada por Nicho** - Valor agregado
4. **Sistema de Planos** - Monetização

**Minha sugestão:** Começar com **Sistema de Tenants e Instâncias** porque é a base de tudo!

---

**Última atualização:** 13/12/2024

