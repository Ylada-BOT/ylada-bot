# 🚀 Plano de Desenvolvimento - Modelo Híbrido de Precificação IA

## 🎯 OBJETIVO

Implementar sistema completo de precificação híbrida onde:
- Cliente tem limite de mensagens com IA incluído no plano
- Sistema rastreia uso em tempo real
- Cobra excedente automaticamente
- Oferece upgrades quando necessário

---

## 📋 ETAPAS DE DESENVOLVIMENTO

### **FASE 1: Base de Dados e Modelos** (2-3 dias)

#### 1.1 Criar Modelo de Uso de IA
- [ ] Criar tabela `ia_usage` no banco
  - `tenant_id` (FK)
  - `instance_id` (FK, opcional)
  - `date` (data)
  - `messages_count` (número de mensagens)
  - `tokens_used` (tokens consumidos)
  - `cost` (custo real)
  - `created_at`

- [ ] Criar modelo `IAUsage` em `src/models/ia_usage.py`

**Arquivo:** `src/models/ia_usage.py`

```python
class IAUsage(Base):
    __tablename__ = 'ia_usage'
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    instance_id = Column(Integer, ForeignKey('instances.id'), nullable=True)
    date = Column(Date, nullable=False)
    messages_count = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

#### 1.2 Adicionar Campos ao Modelo Plan
- [ ] Adicionar `messages_included` (mensagens incluídas)
- [ ] Adicionar `excess_price_per_message` (preço do excedente)
- [ ] Adicionar `hard_limit_multiplier` (ex: 1.5 = 150% do limite)

**Arquivo:** `src/models/subscription.py`

```python
# Adicionar ao modelo Plan
messages_included = Column(Integer, default=1000)  # Mensagens com IA incluídas
excess_price_per_message = Column(Float, default=0.15)  # Preço por msg excedente
hard_limit_multiplier = Column(Float, default=1.5)  # 150% = hard limit
```

---

#### 1.3 Criar Modelo de Limites
- [ ] Criar tabela `usage_limits` para rastrear limites por tenant
  - `tenant_id`
  - `current_month_messages` (contador do mês atual)
  - `limit_reset_date` (data de reset)
  - `last_updated`

**Arquivo:** `src/models/usage_limits.py`

---

### **FASE 2: Sistema de Rastreamento** (3-4 dias)

#### 2.1 Criar Serviço de Rastreamento
- [ ] Criar `src/services/ia_tracker.py`
  - Função `track_ia_usage(tenant_id, tokens_used, cost)`
  - Função `get_current_usage(tenant_id)`
  - Função `check_limit(tenant_id)`
  - Função `reset_monthly_usage(tenant_id)`

**Arquivo:** `src/services/ia_tracker.py`

```python
def track_ia_usage(tenant_id, instance_id, tokens_used, cost):
    """Registra uso de IA"""
    # Incrementa contador do mês
    # Salva no banco
    # Verifica limites
    pass

def get_current_usage(tenant_id):
    """Retorna uso atual do mês"""
    # Busca do banco
    # Retorna: messages_count, limit, percentage
    pass

def check_limit(tenant_id):
    """Verifica se excedeu limite"""
    # Retorna: within_limit, soft_limit, hard_limit
    pass
```

---

#### 2.2 Integrar no AI Handler
- [ ] Modificar `src/ai_handler.py`
  - Rastrear uso após cada resposta
  - Calcular tokens usados
  - Calcular custo real
  - Chamar `ia_tracker.track_ia_usage()`

**Arquivo:** `src/ai_handler.py`

```python
# No método get_response()
def get_response(self, phone: str, message: str):
    # ... código existente ...
    
    # Rastrear uso
    tokens_used = response.usage.total_tokens
    cost = self._calculate_cost(tokens_used)
    
    # Registrar uso
    from src.services.ia_tracker import track_ia_usage
    track_ia_usage(
        tenant_id=tenant_id,
        instance_id=instance_id,
        tokens_used=tokens_used,
        cost=cost
    )
    
    return response
```

---

#### 2.3 Integrar no Message Handler
- [ ] Modificar `src/whatsapp/message_handler.py`
  - Passar `tenant_id` e `instance_id` para AI Handler
  - Verificar limites antes de processar
  - Bloquear se exceder hard limit

---

### **FASE 3: Sistema de Limites e Bloqueios** (2-3 dias)

#### 3.1 Criar Serviço de Limites
- [ ] Criar `src/services/limit_manager.py`
  - Função `check_soft_limit(tenant_id)` - 80% do limite
  - Função `check_hard_limit(tenant_id)` - 150% do limite
  - Função `block_if_exceeded(tenant_id)`
  - Função `allow_with_charge(tenant_id)` - permite mas cobra

**Arquivo:** `src/services/limit_manager.py`

```python
def check_soft_limit(tenant_id):
    """Verifica se chegou em 80% do limite"""
    usage = get_current_usage(tenant_id)
    plan = get_tenant_plan(tenant_id)
    
    percentage = (usage.messages_count / plan.messages_included) * 100
    
    if percentage >= 80:
        send_soft_limit_alert(tenant_id)
        return True
    return False

def check_hard_limit(tenant_id):
    """Verifica se excedeu hard limit (150%)"""
    usage = get_current_usage(tenant_id)
    plan = get_tenant_plan(tenant_id)
    
    hard_limit = plan.messages_included * plan.hard_limit_multiplier
    
    if usage.messages_count >= hard_limit:
        block_tenant(tenant_id)
        return True
    return False
```

---

#### 3.2 Implementar Bloqueio
- [ ] Criar função `block_tenant(tenant_id)`
- [ ] Criar função `unblock_tenant(tenant_id)`
- [ ] Adicionar campo `is_blocked` no modelo Tenant
- [ ] Verificar bloqueio antes de processar mensagem

---

### **FASE 4: Dashboard e Interface** (4-5 dias)

#### 4.1 Dashboard de Uso
- [ ] Criar página `web/templates/usage/dashboard.html`
  - Gráfico de uso do mês
  - Barra de progresso
  - Mensagens usadas / limite
  - Percentual usado
  - Alertas visuais (80%, 100%)

**Arquivo:** `web/templates/usage/dashboard.html`

```html
<div class="usage-dashboard">
    <h2>Uso de IA este mês</h2>
    
    <div class="usage-meter">
        <div class="progress-bar">
            <div class="progress" style="width: 70%"></div>
        </div>
        <p>3.500 / 5.000 mensagens (70%)</p>
    </div>
    
    <div class="alerts">
        <div class="alert warning" v-if="usage >= 80">
            ⚠️ Você está em 80% do limite
        </div>
        <div class="alert danger" v-if="usage >= 100">
            ⛔ Limite excedido! Upgrade necessário
        </div>
    </div>
    
    <button class="btn-upgrade">Fazer Upgrade</button>
</div>
```

---

#### 4.2 API de Uso
- [ ] Criar `web/api/usage.py`
  - `GET /api/usage/current` - Uso atual
  - `GET /api/usage/history` - Histórico
  - `GET /api/usage/stats` - Estatísticas

**Arquivo:** `web/api/usage.py`

```python
@bp.route('/current', methods=['GET'])
@require_api_auth
def get_current_usage():
    tenant_id = get_current_tenant_id()
    usage = ia_tracker.get_current_usage(tenant_id)
    plan = get_tenant_plan(tenant_id)
    
    return jsonify({
        'messages_used': usage.messages_count,
        'messages_limit': plan.messages_included,
        'percentage': (usage.messages_count / plan.messages_included) * 100,
        'excess_messages': max(0, usage.messages_count - plan.messages_included),
        'excess_cost': calculate_excess_cost(tenant_id)
    })
```

---

#### 4.3 Componente de Uso no Dashboard
- [ ] Adicionar card de uso no dashboard principal
- [ ] Atualizar em tempo real (polling ou WebSocket)
- [ ] Mostrar alertas visuais

---

### **FASE 5: Sistema de Cobrança** (3-4 dias)

#### 5.1 Criar Serviço de Cobrança
- [ ] Criar `src/services/billing.py`
  - Função `calculate_monthly_bill(tenant_id)`
  - Função `calculate_excess_charge(tenant_id)`
  - Função `generate_invoice(tenant_id)`

**Arquivo:** `src/services/billing.py`

```python
def calculate_monthly_bill(tenant_id):
    """Calcula fatura mensal"""
    plan = get_tenant_plan(tenant_id)
    usage = get_current_usage(tenant_id)
    
    base_price = plan.price
    
    # Calcular excedente
    if usage.messages_count > plan.messages_included:
        excess = usage.messages_count - plan.messages_included
        excess_charge = excess * plan.excess_price_per_message
    else:
        excess_charge = 0
    
    return {
        'base_price': base_price,
        'excess_messages': excess,
        'excess_charge': excess_charge,
        'total': base_price + excess_charge
    }
```

---

#### 5.2 Integrar com Gateway de Pagamento
- [ ] Criar função `charge_excess(tenant_id, amount)`
- [ ] Integrar com Stripe/Mercado Pago
- [ ] Criar invoice automático no final do mês

---

#### 5.3 Histórico de Faturas
- [ ] Criar tabela `invoices`
- [ ] Criar modelo `Invoice`
- [ ] Interface para ver faturas anteriores

---

### **FASE 6: Alertas e Notificações** (2-3 dias)

#### 6.1 Sistema de Alertas
- [ ] Criar `src/services/alert_service.py`
  - Alerta em 80% (soft limit)
  - Alerta em 100% (limite atingido)
  - Alerta em 150% (hard limit - bloqueio)

**Arquivo:** `src/services/alert_service.py`

```python
def send_soft_limit_alert(tenant_id):
    """Envia alerta quando chega em 80%"""
    # Envia email
    # Envia notificação no dashboard
    # Envia WhatsApp (se configurado)
    pass

def send_hard_limit_alert(tenant_id):
    """Envia alerta quando excede hard limit"""
    # Bloqueia tenant
    # Notifica urgente
    # Oferece upgrade imediato
    pass
```

---

#### 6.2 Notificações no Dashboard
- [ ] Sistema de notificações em tempo real
- [ ] Badge de alerta
- [ ] Modal de upgrade quando necessário

---

### **FASE 7: Sistema de Upgrade** (2-3 dias)

#### 7.1 Sugestão Automática de Upgrade
- [ ] Criar função `suggest_upgrade(tenant_id)`
- [ ] Mostrar quando uso > 80%
- [ ] Comparar planos disponíveis

---

#### 7.2 Processo de Upgrade
- [ ] Interface de upgrade
- [ ] Calcular diferença de preço
- [ ] Aplicar upgrade imediatamente
- [ ] Ajustar limites

---

### **FASE 8: Cache e Otimização** (3-4 dias)

#### 8.1 Sistema de Cache
- [ ] Criar `src/services/response_cache.py`
- [ ] Cache de respostas similares
- [ ] Reduzir chamadas à IA

**Arquivo:** `src/services/response_cache.py`

```python
def get_cached_response(message, tenant_id):
    """Busca resposta em cache"""
    # Hash da mensagem
    # Busca no Redis/cache
    # Retorna se encontrado
    pass

def cache_response(message, response, tenant_id):
    """Salva resposta no cache"""
    # Hash da mensagem
    # Salva no Redis/cache
    # TTL de 24h
    pass
```

---

#### 8.2 Otimizações
- [ ] Usar modelo mais barato (gpt-4o-mini)
- [ ] Limitar tokens por resposta
- [ ] Respostas pré-definidas para FAQs

---

## 📅 CRONOGRAMA ESTIMADO

| Fase | Tarefas | Tempo | Prioridade |
|------|---------|-------|------------|
| **Fase 1** | Base de Dados | 2-3 dias | ⭐⭐⭐⭐⭐ Crítica |
| **Fase 2** | Rastreamento | 3-4 dias | ⭐⭐⭐⭐⭐ Crítica |
| **Fase 3** | Limites | 2-3 dias | ⭐⭐⭐⭐ Alta |
| **Fase 4** | Dashboard | 4-5 dias | ⭐⭐⭐⭐ Alta |
| **Fase 5** | Cobrança | 3-4 dias | ⭐⭐⭐ Média |
| **Fase 6** | Alertas | 2-3 dias | ⭐⭐⭐ Média |
| **Fase 7** | Upgrade | 2-3 dias | ⭐⭐ Baixa |
| **Fase 8** | Cache | 3-4 dias | ⭐⭐ Baixa |
| **TOTAL** | - | **21-29 dias** | - |

---

## 🎯 PRIORIDADES

### **MVP (Mínimo Viável) - 2 semanas**

1. ✅ Fase 1: Base de Dados (2-3 dias)
2. ✅ Fase 2: Rastreamento (3-4 dias)
3. ✅ Fase 3: Limites Básicos (2 dias)
4. ✅ Fase 4: Dashboard Básico (3 dias)

**Total MVP:** 10-12 dias

---

### **Versão Completa - 4 semanas**

1. ✅ Todas as fases acima
2. ✅ Fase 5: Cobrança (3-4 dias)
3. ✅ Fase 6: Alertas (2-3 dias)
4. ✅ Fase 7: Upgrade (2-3 dias)
5. ✅ Fase 8: Cache (3-4 dias)

**Total Completo:** 21-29 dias

---

## 🛠️ ARQUIVOS A CRIAR/MODIFICAR

### **Novos Arquivos:**
- [ ] `src/models/ia_usage.py`
- [ ] `src/models/usage_limits.py`
- [ ] `src/models/invoice.py`
- [ ] `src/services/ia_tracker.py`
- [ ] `src/services/limit_manager.py`
- [ ] `src/services/billing.py`
- [ ] `src/services/alert_service.py`
- [ ] `src/services/response_cache.py`
- [ ] `web/api/usage.py`
- [ ] `web/templates/usage/dashboard.html`

### **Arquivos a Modificar:**
- [ ] `src/models/subscription.py` (adicionar campos)
- [ ] `src/models/tenant.py` (adicionar is_blocked)
- [ ] `src/ai_handler.py` (integrar rastreamento)
- [ ] `src/whatsapp/message_handler.py` (verificar limites)
- [ ] `web/templates/dashboard.html` (adicionar card de uso)

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### **Semana 1: Base**
- [ ] Criar modelos de banco de dados
- [ ] Migração do banco
- [ ] Serviço de rastreamento básico
- [ ] Integrar no AI Handler

### **Semana 2: Limites e Dashboard**
- [ ] Sistema de limites
- [ ] Dashboard de uso
- [ ] API de uso
- [ ] Alertas básicos

### **Semana 3: Cobrança**
- [ ] Sistema de cobrança
- [ ] Integração com pagamento
- [ ] Histórico de faturas
- [ ] Testes

### **Semana 4: Otimizações**
- [ ] Sistema de cache
- [ ] Otimizações de IA
- [ ] Sistema de upgrade
- [ ] Polimento final

---

## 🚀 COMEÇAR AGORA?

**Sugestão:** Começar pela **Fase 1 (Base de Dados)** que é a fundação de tudo!

Quer que eu comece criando os modelos de banco de dados?

---

**Última atualização:** 13/12/2024


