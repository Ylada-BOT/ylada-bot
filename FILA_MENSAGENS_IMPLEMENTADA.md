# ✅ Fila de Mensagens Implementada

**Data:** 2025-01-27  
**Status:** ✅ Implementado (pendente instalação de dependências)

---

## 🎯 O QUE FOI FEITO

### **1. Sistema de Fila de Mensagens** ✅
- **Arquivo:** `web/utils/message_queue.py`
- **Funcionalidades:**
  - Fila persistente (Redis ou memória)
  - Priorização de mensagens
  - Retry automático em falhas
  - Status de mensagens (pending, processing, sent, failed, retrying)
  - Suporte a múltiplos tenants/instâncias

### **2. Worker de Processamento** ✅
- **Arquivo:** `web/workers/message_worker.py`
- **Funcionalidades:**
  - Processa mensagens em background
  - Retry automático com backoff
  - Rate limiting integrado
  - Logs detalhados
  - Estatísticas de processamento

### **3. Helper de Envio** ✅
- **Arquivo:** `web/utils/message_sender.py`
- **Funcionalidades:**
  - Função centralizada para envio de mensagens
  - Usa fila automaticamente (com fallback para envio direto)
  - Suporte a prioridades
  - Integração transparente

### **4. Integração no App** ✅
- **Arquivo:** `web/app.py`
- Integração:
  - Inicialização automática da fila
  - Worker iniciado em thread separada
  - Webhook usa fila para envio de respostas

---

## 📋 FUNCIONALIDADES

### **1. Fila de Mensagens**

#### **Adicionar Mensagem à Fila**
```python
from web.utils.message_queue import get_message_queue

queue = get_message_queue()
message_id = queue.add_message(
    phone="5511999999999",
    message="Olá!",
    tenant_id=1,
    instance_id=1,
    priority=0,  # Maior = mais prioritário
    max_retries=3,
    retry_delay=5  # Segundos entre tentativas
)
```

#### **Status da Fila**
```python
queue_size = queue.get_queue_size()
processing = queue.get_processing_count()
```

### **2. Worker de Processamento**

O worker processa mensagens automaticamente em background:
- Processa mensagens em ordem de prioridade
- Retry automático em falhas
- Rate limiting integrado
- Logs detalhados

### **3. Helper de Envio**

#### **Enviar Mensagem (Recomendado)**
```python
from web.utils.message_sender import send_message_via_queue

result = send_message_via_queue(
    phone="5511999999999",
    message="Olá!",
    tenant_id=1,
    priority=1,
    use_queue=True  # Usa fila (padrão)
)

if result['success']:
    if result.get('via_queue'):
        print(f"Mensagem adicionada à fila: {result['message_id']}")
    else:
        print("Mensagem enviada diretamente")
```

---

## 🔧 CONFIGURAÇÃO

### **1. Redis (Recomendado para Produção)**

No `.env.local`:
```env
USE_REDIS=true
REDIS_URL=redis://localhost:6379/0
```

**Vantagens do Redis:**
- Persistência entre reinicializações
- Compartilhado entre múltiplas instâncias
- Melhor performance
- Expiração automática de mensagens antigas

### **2. Memória (Desenvolvimento)**

Se não configurar Redis, usa memória:
- Funciona imediatamente
- Não persiste entre reinicializações
- Adequado para desenvolvimento/testes

---

## 📊 FLUXO DE PROCESSAMENTO

```
1. Mensagem adicionada à fila
   ↓
2. Worker pega mensagem (maior prioridade primeiro)
   ↓
3. Worker tenta enviar via WhatsApp
   ↓
4a. Sucesso → Marca como "sent"
4b. Falha → Agenda retry (se tentativas < max_retries)
4c. Máximo de tentativas → Marca como "failed"
```

---

## 🔄 RETRY AUTOMÁTICO

### **Configuração de Retry**
- **max_retries:** Máximo de tentativas (padrão: 3)
- **retry_delay:** Delay entre tentativas em segundos (padrão: 5)

### **Estratégia de Retry**
- Retry automático em falhas
- Delay configurável entre tentativas
- Máximo de tentativas configurável
- Mensagens falhadas são marcadas como "failed"

---

## 📈 PRIORIDADES

### **Sistema de Prioridades**
- **Maior número = maior prioridade**
- Mensagens com maior prioridade são processadas primeiro
- Útil para mensagens urgentes

### **Exemplos**
- **Prioridade 0:** Mensagens normais
- **Prioridade 1:** Respostas automáticas
- **Prioridade 5:** Notificações importantes
- **Prioridade 10:** Mensagens críticas

---

## 🚀 COMO USAR

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Configurar Redis (Opcional)**
```env
USE_REDIS=true
REDIS_URL=redis://localhost:6379/0
```

### **3. Usar Helper de Envio**
```python
from web.utils.message_sender import send_message_via_queue

result = send_message_via_queue(
    phone="5511999999999",
    message="Olá!",
    tenant_id=1
)
```

---

## ⚠️ IMPORTANTE

### **Worker em Background**
O worker roda em thread separada e processa mensagens continuamente. Não precisa fazer nada manualmente.

### **Fallback Automático**
Se a fila não estiver disponível, o sistema faz fallback para envio direto automaticamente.

### **Persistência**
- **Redis:** Mensagens persistem entre reinicializações
- **Memória:** Mensagens são perdidas ao reiniciar

---

## 📊 ESTATÍSTICAS

### **Obter Estatísticas do Worker**
```python
from web.workers.message_worker import get_message_worker

worker = get_message_worker()
if worker:
    stats = worker.get_stats()
    print(f"Processadas: {stats['processed']}")
    print(f"Falhadas: {stats['failed']}")
    print(f"Fila: {stats['queue_size']}")
```

---

## 🐛 TROUBLESHOOTING

### **Mensagens não estão sendo processadas**
1. Verifique se o worker está rodando
2. Verifique se WhatsApp está conectado
3. Verifique logs do worker

### **Mensagens ficam na fila**
1. Verifique se WhatsApp está conectado
2. Verifique se há erros nos logs
3. Verifique rate limiting

### **Redis não conecta**
- Sistema faz fallback automático para memória
- Verifique URL do Redis no `.env.local`
- Verifique se Redis está rodando

---

## 📝 PRÓXIMOS PASSOS

1. ✅ **Fila de Mensagens** - Implementado
2. ✅ **Rate Limiting** - Implementado
3. ⏳ **Monitoramento** - Adicionar dashboard
4. ⏳ **Webhooks de Status** - Notificar status de entrega
5. ⏳ **Analytics** - Métricas de envio

---

**Última atualização:** 2025-01-27



