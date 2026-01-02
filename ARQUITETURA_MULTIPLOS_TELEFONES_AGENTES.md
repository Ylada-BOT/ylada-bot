# 🏗️ Arquitetura: Múltiplos Telefones e Sistema de Agentes

## 📋 VISÃO GERAL

Este documento explica como funciona a integração de múltiplos telefones (robôs) e o sistema de agentes na plataforma YLADA BOT.

---

## 🎯 ESTRUTURA HIERÁRQUICA

```
👤 USUÁRIO (User)
│
└── 🏢 ORGANIZAÇÃO (Tenant)
    │
    ├── 📱 TELEFONE 1 (Instance) - "Bot Vendas"
    │   ├── 🔄 Fluxos específicos deste telefone
    │   ├── 🤖 Agente configurado (IA + comportamento)
    │   └── 💬 Conversas deste telefone
    │
    ├── 📱 TELEFONE 2 (Instance) - "Bot Suporte"
    │   ├── 🔄 Fluxos específicos deste telefone
    │   ├── 🤖 Agente configurado (IA + comportamento)
    │   └── 💬 Conversas deste telefone
    │
    └── 🔄 FLUXOS COMPARTILHADOS (da Organização)
        └── Podem ser usados por qualquer telefone
```

---

## 🔄 MODELO DE FLUXOS

### **Opção 1: Fluxos por Telefone (Recomendado)**

Cada telefone (Instance) pode ter seus próprios fluxos específicos, além de poder usar fluxos compartilhados da organização.

**Vantagens:**
- ✅ Cada telefone pode ter comportamento único
- ✅ Flexibilidade total
- ✅ Fluxos podem ser reutilizados quando necessário

**Exemplo:**
- Telefone "Vendas" → tem fluxos: "Boas-vindas Vendas", "Cardápio", "Finalizar Pedido"
- Telefone "Suporte" → tem fluxos: "Boas-vindas Suporte", "Abertura de Chamado", "FAQ"
- Organização → tem fluxo compartilhado: "Promoção Black Friday" (usado por ambos)

### **Opção 2: Fluxos Compartilhados (Atual)**

Todos os fluxos da organização são compartilhados entre todos os telefones.

**Vantagens:**
- ✅ Simples de gerenciar
- ✅ Mudanças afetam todos os telefones

**Desvantagens:**
- ❌ Menos flexibilidade
- ❌ Difícil ter comportamentos diferentes por telefone

---

## 🤖 SISTEMA DE AGENTES

### **O que é um Agente?**

Um **Agente** é uma configuração de IA + comportamento que define como o bot responde quando não há fluxo ativo ou quando um fluxo usa `ai_response`.

### **Tipos de Agente:**

#### **1. Agente Padrão (Default)**
- Usa a configuração de IA da organização
- Comportamento genérico

#### **2. Agente Especializado**
- Configuração específica para um tipo de atendimento
- Exemplos:
  - **Agente Vendas**: Focado em converter leads, vender produtos
  - **Agente Suporte**: Focado em resolver problemas, tirar dúvidas
  - **Agente Atendimento**: Focado em agendar, informar horários

#### **3. Agente Personalizado**
- Usuário cria seu próprio agente
- Define:
  - System prompt personalizado
  - Modelo de IA (GPT-4, Claude, etc)
  - Temperatura/parâmetros
  - Comportamento específico

### **Como Funciona:**

```
Mensagem chega no Telefone
    ↓
Verifica se há fluxo ativo
    ↓
Se SIM → Executa fluxo
    ↓
Se fluxo tem "ai_response" → Usa Agente do Telefone
    ↓
Se NÃO há fluxo → Usa Agente do Telefone como fallback
```

---

## 📱 MÚLTIPLOS TELEFONES POR USUÁRIO

### **Como Funciona:**

1. **Usuário cria Organização**
   - Exemplo: "Minha Loja"

2. **Usuário adiciona Telefones**
   - Telefone 1: "Bot Vendas" → WhatsApp (11) 99999-1111
   - Telefone 2: "Bot Suporte" → WhatsApp (11) 99999-2222
   - Telefone 3: "Bot Delivery" → WhatsApp (11) 99999-3333

3. **Cada Telefone é Independente**
   - ✅ Conexão WhatsApp própria
   - ✅ Conversas próprias
   - ✅ Fluxos próprios (ou compartilhados)
   - ✅ Agente próprio
   - ✅ Configurações próprias

4. **Mas Compartilham:**
   - ✅ Mesma organização
   - ✅ Mesmos leads (opcional)
   - ✅ Fluxos compartilhados (opcional)
   - ✅ Configurações gerais da organização

---

## 🎨 IMPLEMENTAÇÃO PROPOSTA

### **1. Associação Flow ↔ Instance**

Adicionar campo opcional `instance_id` na tabela `flows`:

```sql
ALTER TABLE flows ADD COLUMN instance_id INTEGER REFERENCES instances(id);
```

**Comportamento:**
- Se `instance_id` = NULL → Fluxo compartilhado (todos os telefones podem usar)
- Se `instance_id` = X → Fluxo específico do telefone X

### **2. Tabela de Agentes**

Criar tabela `agents`:

```sql
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    instance_id INTEGER REFERENCES instances(id), -- NULL = agente padrão da org
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Configuração de IA
    provider VARCHAR(50), -- openai, anthropic, etc
    model VARCHAR(100), -- gpt-4o-mini, claude-3-haiku, etc
    system_prompt TEXT,
    temperature FLOAT DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    
    -- Comportamento
    behavior_config JSON, -- Configurações extras
    
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### **3. Associação Instance ↔ Agent**

Cada Instance (telefone) pode ter um agente configurado:

```sql
ALTER TABLE instances ADD COLUMN agent_id INTEGER REFERENCES agents(id);
```

---

## 🔧 FLUXO DE PROCESSAMENTO ATUALIZADO

```
1. Mensagem chega no WhatsApp
   ↓
2. Identifica Instance (telefone) que recebeu
   ↓
3. Busca fluxos:
   - Fluxos específicos da Instance (instance_id = X)
   - Fluxos compartilhados (instance_id = NULL) da Organization
   ↓
4. Verifica triggers de cada fluxo
   ↓
5. Se trigger ativado:
   - Executa fluxo
   - Se fluxo tem "ai_response" → usa Agente da Instance
   ↓
6. Se nenhum fluxo ativado:
   - Usa Agente da Instance como fallback
   - Responde com IA
```

---

## 📊 EXEMPLO PRÁTICO COMPLETO

### **Cenário: Loja de Roupas**

```
👤 João Silva (User)
│
└── 🏢 Loja de Roupas ABC (Organization)
    │
    ├── 📱 Telefone 1: "Bot Vendas"
    │   ├── WhatsApp: (11) 98765-4321
    │   ├── 🤖 Agente: "Vendedor Amigável"
    │   │   └── System Prompt: "Você é um vendedor de roupas..."
    │   │
    │   └── 🔄 Fluxos:
    │       ├── "Boas-vindas Vendas" (específico)
    │       ├── "Mostrar Catálogo" (específico)
    │       └── "Promoção Black Friday" (compartilhado)
    │
    ├── 📱 Telefone 2: "Bot Suporte"
    │   ├── WhatsApp: (11) 98765-4322
    │   ├── 🤖 Agente: "Atendente Suporte"
    │   │   └── System Prompt: "Você é um atendente de suporte..."
    │   │
    │   └── 🔄 Fluxos:
    │       ├── "Abertura de Chamado" (específico)
    │       ├── "FAQ" (específico)
    │       └── "Promoção Black Friday" (compartilhado)
    │
    └── 🔄 Fluxos Compartilhados:
        └── "Promoção Black Friday" (usado por ambos)
```

### **Como Funciona na Prática:**

1. **Cliente manda "oi" no Telefone Vendas:**
   - ✅ Ativa fluxo "Boas-vindas Vendas"
   - ✅ Responde: "Olá! Bem-vindo à nossa loja de roupas..."

2. **Cliente manda "oi" no Telefone Suporte:**
   - ✅ Ativa fluxo "Abertura de Chamado" (se configurado)
   - ✅ Ou usa Agente "Atendente Suporte"
   - ✅ Responde: "Olá! Como posso ajudar com seu problema?"

3. **Cliente manda "promoção" em qualquer telefone:**
   - ✅ Ativa fluxo compartilhado "Promoção Black Friday"
   - ✅ Responde com informações da promoção

---

## 🚀 PRÓXIMOS PASSOS DE IMPLEMENTAÇÃO

### **Fase 1: Associação Flow ↔ Instance**
- [ ] Adicionar campo `instance_id` na tabela `flows`
- [ ] Atualizar `Flow` model
- [ ] Atualizar `MessageHandler` para filtrar fluxos por instance
- [ ] Atualizar interface para associar fluxos a telefones

### **Fase 2: Sistema de Agentes**
- [ ] Criar tabela `agents`
- [ ] Criar model `Agent`
- [ ] Criar API para gerenciar agentes
- [ ] Atualizar `AIHandler` para usar agentes
- [ ] Interface para criar/configurar agentes

### **Fase 3: Associação Instance ↔ Agent**
- [ ] Adicionar campo `agent_id` na tabela `instances`
- [ ] Atualizar `Instance` model
- [ ] Atualizar `MessageHandler` para usar agente da instance
- [ ] Interface para selecionar agente por telefone

### **Fase 4: Interface de Gerenciamento**
- [ ] Interface para gerenciar múltiplos telefones
- [ ] Interface para associar fluxos a telefones
- [ ] Interface para configurar agentes por telefone
- [ ] Dashboard mostrando todos os telefones

---

## ❓ PERGUNTAS FREQUENTES

### **1. Um fluxo pode ser usado por vários telefones?**
✅ **SIM!** Se o fluxo tiver `instance_id = NULL`, ele é compartilhado e pode ser usado por todos os telefones da organização.

### **2. Um telefone pode ter vários agentes?**
❌ **NÃO diretamente.** Cada telefone tem UM agente principal. Mas você pode criar fluxos específicos que usam diferentes comportamentos.

### **3. Como escolher qual agente usar?**
Você pode:
- **Configurar agente padrão** para cada telefone
- **Criar agentes especializados** e associar a telefones específicos
- **Usar agentes em fluxos** específicos (futuro)

### **4. Posso ter fluxos diferentes para cada telefone?**
✅ **SIM!** Basta criar fluxos com `instance_id` específico. Cada telefone terá seus próprios fluxos + fluxos compartilhados.

### **5. Como funciona quando um usuário tem vários telefones?**
Cada telefone funciona de forma **independente**:
- Conexão WhatsApp própria
- Conversas próprias
- Fluxos próprios (ou compartilhados)
- Agente próprio

Mas todos compartilham a mesma **organização** e podem usar **fluxos compartilhados**.

---

## 📝 RESUMO

| Recurso | Status Atual | Proposta |
|---------|--------------|----------|
| Múltiplos telefones por organização | ✅ Implementado | ✅ Manter |
| Fluxos por telefone | ❌ Não implementado | ✅ Adicionar `instance_id` opcional |
| Fluxos compartilhados | ✅ Implementado | ✅ Manter |
| Sistema de agentes | ❌ Não implementado | ✅ Criar tabela `agents` |
| Agente por telefone | ❌ Não implementado | ✅ Adicionar `agent_id` em `instances` |
| Interface de gerenciamento | ⚠️ Parcial | ✅ Melhorar |

---

**Última atualização:** 2024-12-23


