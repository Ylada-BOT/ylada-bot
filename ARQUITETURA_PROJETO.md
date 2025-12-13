# 🏗️ ARQUITETURA DO PROJETO - BOT by YLADA

## 📋 VISÃO GERAL

Sistema SaaS multi-tenant para automação de WhatsApp com IA, fluxos de vendas, captação de leads e notificações.

---

## 🎯 OBJETIVOS

1. **Multi-tenant**: Cada cliente isolado
2. **Automações**: Fluxos visuais de vendas/suporte
3. **IA Integrada**: Respostas inteligentes
4. **Captação**: Leads automáticos
5. **Notificações**: Alertas para outro WhatsApp
6. **Métricas**: Dashboard de resultados
7. **Pagamento**: Assinaturas e planos
8. **API Pública**: Integrações externas

---

## 📁 ESTRUTURA DE PASTAS

```
Ylada BOT/
├── src/
│   ├── models/              # Modelos de banco de dados
│   │   ├── __init__.py
│   │   ├── user.py          # Usuários/revendedores
│   │   ├── tenant.py        # Clientes finais (multi-tenant)
│   │   ├── subscription.py  # Assinaturas e planos
│   │   ├── instance.py      # Instâncias WhatsApp
│   │   ├── flow.py          # Fluxos de automação
│   │   ├── conversation.py  # Conversas
│   │   ├── lead.py          # Leads capturados
│   │   └── notification.py  # Notificações
│   │
│   ├── database/            # Configuração do banco
│   │   ├── __init__.py
│   │   ├── db.py            # Conexão SQLAlchemy
│   │   └── migrations/      # Migrações Alembic
│   │
│   ├── auth/                # Autenticação
│   │   ├── __init__.py
│   │   ├── authentication.py  # Login/registro
│   │   └── authorization.py  # Permissões
│   │
│   ├── flows/               # Motor de fluxos
│   │   ├── __init__.py
│   │   ├── flow_engine.py   # Executa fluxos
│   │   ├── flow_builder.py  # Construtor visual
│   │   ├── flow_executor.py # Executa ações
│   │   └── templates.py      # Templates prontos
│   │
│   ├── actions/             # Ações dos fluxos
│   │   ├── __init__.py
│   │   ├── send_message.py
│   │   ├── wait.py
│   │   ├── condition.py
│   │   ├── webhook.py
│   │   └── ai_response.py
│   │
│   ├── leads/               # Captação de leads
│   │   ├── __init__.py
│   │   ├── lead_capture.py
│   │   ├── lead_scoring.py
│   │   └── lead_tracking.py
│   │
│   ├── notifications/       # Sistema de notificações
│   │   ├── __init__.py
│   │   ├── notification_manager.py
│   │   ├── notification_rules.py
│   │   └── notification_sender.py
│   │
│   ├── analytics/           # Métricas e analytics
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   └── reports.py
│   │
│   ├── payments/            # Sistema de pagamento
│   │   ├── __init__.py
│   │   ├── payment_gateway.py
│   │   └── subscription_manager.py
│   │
│   ├── whatsapp/            # Integração WhatsApp
│   │   ├── __init__.py
│   │   ├── instance_manager.py
│   │   ├── message_handler.py
│   │   └── message_sender.py
│   │
│   ├── api/                 # API pública
│   │   ├── __init__.py
│   │   ├── webhooks.py
│   │   └── rest_api.py
│   │
│   ├── whatsapp_webjs_handler.py  # Handler atual (manter)
│   └── ai_handler.py              # Handler IA atual (manter)
│
├── web/
│   ├── app.py               # App Flask principal
│   ├── api/                 # Rotas da API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tenants.py
│   │   ├── flows.py
│   │   ├── conversations.py
│   │   ├── leads.py
│   │   ├── analytics.py
│   │   └── payments.py
│   │
│   ├── templates/           # Templates HTML
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard.html
│   │   ├── flows/
│   │   │   ├── builder.html
│   │   │   └── list.html
│   │   ├── conversations.html
│   │   ├── leads.html
│   │   ├── analytics.html
│   │   └── settings.html
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── assets/
│
├── config/
│   ├── __init__.py
│   ├── settings.py          # Configurações gerais
│   └── database.py          # Config DB
│
├── data/                    # Dados locais
│   ├── sessions/            # Sessões WhatsApp
│   └── uploads/             # Uploads de arquivos
│
├── requirements.txt
├── package.json
├── whatsapp_server.js
└── .env.example
```

---

## 🗄️ BANCO DE DADOS (PostgreSQL)

### Tabelas Principais

1. **users** - Usuários/revendedores
   - id, email, password_hash, name, role, created_at

2. **tenants** - Clientes finais (multi-tenant)
   - id, user_id, name, subdomain, plan_id, status, created_at

3. **subscriptions** - Assinaturas
   - id, tenant_id, plan_id, status, start_date, end_date, payment_method

4. **plans** - Planos de assinatura
   - id, name, price, max_instances, max_flows, max_messages_month, features

5. **instances** - Instâncias WhatsApp
   - id, tenant_id, name, phone_number, status, session_data, created_at

6. **flows** - Fluxos de automação
   - id, tenant_id, name, description, flow_data (JSON), status, created_at

7. **conversations** - Conversas
   - id, tenant_id, instance_id, phone, contact_name, last_message_at, status

8. **messages** - Mensagens
   - id, conversation_id, direction, content, timestamp, flow_id

9. **leads** - Leads capturados
   - id, tenant_id, phone, name, source, score, status, created_at

10. **notifications** - Notificações
    - id, tenant_id, type, message, sent_to, status, created_at

---

## 🔄 FLUXO DE DADOS

```
WhatsApp → whatsapp_server.js → message_handler.py → flow_engine.py → actions → WhatsApp
                                                      ↓
                                              lead_capture.py → leads
                                              notification_manager.py → WhatsApp (gestor)
                                              analytics/metrics.py → dashboard
```

---

## 🚀 IMPLEMENTAÇÃO - ORDEM DE PRIORIDADE

### FASE 1: Fundação (Crítico)
1. ✅ Banco de dados (models + migrations)
2. ✅ Autenticação (login/registro)
3. ✅ Multi-tenant (isolamento de dados)

### FASE 2: Core (Essencial)
4. ✅ Motor de fluxos básico
5. ✅ Sistema de notificações
6. ✅ Captação de leads

### FASE 3: Monetização (Comercial)
7. ✅ Sistema de pagamento
8. ✅ Planos e limites
9. ✅ Dashboard de métricas

### FASE 4: Diferenciais (Competitivo)
10. ✅ Templates prontos
11. ✅ API pública
12. ✅ Analytics avançado

---

## 🛠️ TECNOLOGIAS

- **Backend**: Flask (Python)
- **Database**: PostgreSQL + SQLAlchemy
- **Cache**: Redis (opcional, para performance)
- **Fila**: Celery + Redis (para processamento assíncrono)
- **WhatsApp**: whatsapp-web.js (Node.js)
- **IA**: OpenAI / Anthropic
- **Pagamento**: Stripe / Mercado Pago / Asaas
- **Frontend**: HTML/CSS/JS (pode evoluir para React)

---

## 📝 PRÓXIMOS PASSOS

1. Criar estrutura de pastas
2. Configurar banco de dados
3. Criar models
4. Implementar autenticação
5. Implementar multi-tenant
6. Criar motor de fluxos
7. Integrar tudo

---

**Status**: 🚧 Em construção
