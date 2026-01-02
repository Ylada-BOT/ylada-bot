# ✅ Rate Limiting Implementado

**Data:** 2025-01-27  
**Status:** ✅ Implementado (pendente instalação de dependências)

---

## 🎯 O QUE FOI FEITO

### **1. Módulo de Rate Limiting Criado** ✅
- **Arquivo:** `web/utils/rate_limiter.py`
- **Funcionalidades:**
  - Rate limiting por usuário/tenant/IP
  - Limites específicos para WhatsApp (15 msg/min, 800 msg/dia)
  - Suporte para Redis ou memória
  - Limites baseados em planos (Free, Basic, Pro, Enterprise)

### **2. Integração no App Flask** ✅
- **Arquivo:** `web/app.py`
- Rate limiting aplicado em:
  - `/webhook` - Webhook de mensagens recebidas (envio de respostas)
  - Inicialização automática do rate limiter

### **3. Integração nas APIs** ✅
- **Arquivo:** `web/api/notifications.py`
- Rate limiting aplicado em:
  - `/api/notifications/<id>/send` - Envio individual
  - `/api/notifications/pending/send-all` - Envio em massa

### **4. Dependências Adicionadas** ✅
- **Arquivo:** `requirements.txt`
- Adicionado: `flask-limiter==3.5.0`
- Adicionado: `redis==5.0.1` (para uso futuro)
- Adicionado: `huey==2.5.0` (para fila de mensagens)

---

## 📋 LIMITES CONFIGURADOS

### **Limites do WhatsApp (Conservadores)**
- **15 mensagens/minuto** (abaixo do limite de 20 do WhatsApp)
- **800 mensagens/dia** (abaixo do limite de 1000 do WhatsApp)

### **Limites por Plano**
- **Free/Grátis:** 10 msg/min, 500 msg/dia
- **Basic/Básico:** 15 msg/min, 2000 msg/dia
- **Pro/Profissional:** 20 msg/min, 10000 msg/dia
- **Enterprise:** 50 msg/min, ilimitado

### **Limite Padrão (Outras APIs)**
- **200 requisições/hora** por IP/usuário

---

## 🚀 COMO USAR

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Configurar Redis (Opcional)**
No `.env.local`:
```env
USE_REDIS=true
REDIS_URL=redis://localhost:6379/0
```

**Nota:** Se não configurar Redis, usa memória (funciona, mas não persiste entre reinicializações)

### **3. Aplicar em Novas Rotas**
```python
from web.utils.rate_limiter import rate_limit_whatsapp

@app.route('/api/send-message', methods=['POST'])
@rate_limit_whatsapp
def send_message():
    # Sua lógica aqui
    pass
```

---

## 🔧 FUNCIONALIDADES

### **1. Chave de Rate Limiting**
O sistema identifica usuários por:
1. `user_id` + `tenant_id` (se logado)
2. `user_id` (se logado sem tenant)
3. IP do cliente (fallback)

### **2. Armazenamento**
- **Memória:** Padrão, funciona imediatamente
- **Redis:** Recomendado para produção (persistente, compartilhado entre instâncias)

### **3. Estratégia**
- **Fixed Window:** Janela fixa de tempo
- Exemplo: 15/min = máximo 15 requisições em qualquer janela de 1 minuto

---

## ⚠️ IMPORTANTE

### **Limites Conservadores**
Os limites estão configurados de forma **conservadora** para evitar bloqueios do WhatsApp:
- WhatsApp permite ~20 msg/min, configuramos **15 msg/min**
- WhatsApp permite ~1000 msg/dia, configuramos **800 msg/dia**

### **Ajuste Conforme Necessidade**
Se precisar ajustar limites, edite `web/utils/rate_limiter.py`:
```python
def get_whatsapp_rate_limits():
    return [
        "15 per minute",  # Ajuste aqui
        "800 per day"     # Ajuste aqui
    ]
```

---

## 📊 PRÓXIMOS PASSOS

1. ✅ **Rate Limiting** - Implementado
2. ⏳ **Fila de Mensagens** - Próximo
3. ⏳ **Retry Automático** - Depois
4. ⏳ **Monitoramento** - Depois

---

## 🐛 TROUBLESHOOTING

### **Erro: ModuleNotFoundError: No module named 'flask_limiter'**
```bash
pip install flask-limiter==3.5.0
```

### **Rate limiting não funciona**
- Verifique se `init_rate_limiter()` foi chamado no `app.py`
- Verifique se o decorator `@rate_limit_whatsapp` está aplicado na rota

### **Limites muito restritivos**
- Ajuste os limites em `get_whatsapp_rate_limits()`
- Considere usar Redis para melhor controle

---

**Última atualização:** 2025-01-27



