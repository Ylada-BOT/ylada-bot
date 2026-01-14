# 🚀 Integração Z-API (MAIS RÁPIDO - Brasil)

**Tempo:** 1-2 horas  
**Resultado:** WhatsApp funcionando estável  
**Vantagem:** Suporte em português, preços em R$

---

## ✅ POR QUE Z-API?

1. **Setup mais rápido** - 1-2 horas (vs 1-2 dias Twilio)
2. **Suporte em português** - Fácil comunicação
3. **Preços em R$** - Sem conversão de moeda
4. **API REST simples** - Fácil integrar
5. **Dashboard pronto** - Gerencia tudo visualmente
6. **Múltiplas instâncias** - Vários números WhatsApp

---

## ⚠️ IMPORTANTE SABER

**Z-API usa whatsapp-web.js por trás**, mas:
- ✅ Eles mantêm a infraestrutura (você não precisa)
- ✅ Auto-restart quando quebra
- ✅ Múltiplos servidores (alta disponibilidade)
- ✅ Monitoramento 24/7
- ⚠️ Não é API oficial (risco menor que fazer você mesmo, mas existe)

**Para começar a vender HOJE:** Z-API é perfeito!  
**Para escalar muito:** Considere API oficial depois.

---

## 📋 PASSO A PASSO (1-2 horas)

### **1. Criar Conta Z-API (15 min)**

1. Acesse: https://z-api.io (ou site atual)
2. Crie conta
3. Escolha plano:
   - **Básico:** ~R$ 50-100/mês (1 instância)
   - **Pro:** ~R$ 200-500/mês (múltiplas instâncias)

### **2. Criar Instância WhatsApp (10 min)**

1. No dashboard Z-API: **Instâncias > Nova Instância**
2. Escaneie QR Code
3. Aguarde conectar
4. Anote: `Instance ID` e `Token`

### **3. Integrar com Sua Plataforma (1 hora)**

#### **Backend (Flask):**

```python
# web/utils/zapi_handler.py
import requests
import os

class ZAPIHandler:
    def __init__(self):
        self.base_url = os.getenv('ZAPI_BASE_URL', 'https://api.z-api.io')
        self.instance_id = os.getenv('ZAPI_INSTANCE_ID')
        self.token = os.getenv('ZAPI_TOKEN')
    
    def send_message(self, phone, message):
        """Envia mensagem via Z-API"""
        url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}/send-text"
        
        # Formata número (remove caracteres, adiciona código do país)
        phone = phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not phone.startswith('55'):  # Se não tem código do Brasil
            phone = '55' + phone
        
        payload = {
            "phone": phone,
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return {'success': True, 'message_id': response.json().get('id')}
            else:
                return {'success': False, 'error': response.text}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_qr_code(self):
        """Obtém QR Code para conectar"""
        url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}/qr-code"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {'success': True, 'qr': data.get('base64'), 'qr_code': data.get('qr_code')}
            return {'success': False, 'error': 'QR Code não disponível'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_status(self):
        """Verifica status da conexão"""
        url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}/status"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'connected': data.get('connected', False),
                    'status': data.get('status'),
                    'phone': data.get('phone')
                }
            return {'connected': False, 'error': 'Não foi possível verificar status'}
        except Exception as e:
            return {'connected': False, 'error': str(e)}
```

#### **Rotas Flask:**

```python
# web/app.py
from web.utils.zapi_handler import ZAPIHandler

zapi_handler = ZAPIHandler()

@app.route('/api/whatsapp/send', methods=['POST'])
@require_api_auth
def send_whatsapp():
    """Envia mensagem via Z-API"""
    data = request.get_json()
    result = zapi_handler.send_message(
        phone=data.get('to'),
        message=data.get('message')
    )
    return jsonify(result)

@app.route('/api/whatsapp/qr', methods=['GET'])
@require_api_auth
def get_whatsapp_qr():
    """Obtém QR Code Z-API"""
    result = zapi_handler.get_qr_code()
    return jsonify(result)

@app.route('/api/whatsapp/status', methods=['GET'])
@require_api_auth
def get_whatsapp_status():
    """Status da conexão Z-API"""
    result = zapi_handler.get_status()
    return jsonify(result)

@app.route('/webhook/zapi/whatsapp', methods=['POST'])
def zapi_webhook():
    """Webhook Z-API - recebe mensagens"""
    data = request.get_json()
    
    # Z-API envia mensagens recebidas aqui
    phone = data.get('phone', '').replace('@c.us', '')
    message = data.get('message', {}).get('text', '')
    message_id = data.get('message', {}).get('id')
    
    # Processa com sua IA
    # ... seu código de IA aqui ...
    
    return jsonify({'success': True}), 200
```

### **4. Configurar Webhook (5 min)**

1. No dashboard Z-API: **Webhooks > Configurar**
2. URL do webhook: `https://seu-dominio.com/webhook/zapi/whatsapp`
3. Eventos: Marque "Mensagem recebida"
4. Salve

### **5. Variáveis de Ambiente**

Adicione no `.env`:
```bash
ZAPI_BASE_URL=https://api.z-api.io
ZAPI_INSTANCE_ID=seu_instance_id
ZAPI_TOKEN=seu_token
```

### **6. Testar (15 min)**

```bash
# Testa envio
curl -X POST http://localhost:5002/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_token" \
  -d '{"to": "5511999999999", "message": "Teste Z-API"}'
```

---

## 💰 CUSTO Z-API

- **Plano Básico:** ~R$ 50-100/mês (1 instância)
- **Plano Pro:** ~R$ 200-500/mês (múltiplas instâncias)
- **Geralmente:** Mensagens ilimitadas no plano

**Comparação:**
- Z-API: R$ 50-500/mês (fixo)
- Twilio: $0.005-0.09/msg (pode ficar caro)
- Meta Direto: Grátis + R$ 0,02-0,40/msg

---

## ✅ VANTAGENS Z-API

1. **Mais rápido** - Setup em 1-2 horas
2. **Suporte PT** - Fácil comunicação
3. **Preço fixo** - Sem surpresas
4. **Dashboard** - Gerencia visualmente
5. **Múltiplas instâncias** - Vários números
6. **Webhooks** - Recebe mensagens automaticamente

---

## ⚠️ DESVANTAGENS

1. **Não é oficial** - Risco menor, mas existe
2. **Dependência** - Você depende deles
3. **Pode quebrar** - Se WhatsApp mudar (mas eles mantêm)

---

## 🎯 QUANDO USAR Z-API

✅ **Use Z-API se:**
- Precisa começar HOJE
- Quer suporte em português
- Prefere preço fixo
- Não quer lidar com infraestrutura
- Tem 1-5 números WhatsApp

❌ **Não use Z-API se:**
- Precisa de API oficial (compliance)
- Vai ter milhões de mensagens (pode ficar caro)
- Quer controle total da infraestrutura

---

## 📞 QUER QUE EU IMPLEMENTE Z-API?

Posso criar a integração completa agora:
1. ✅ Handler Z-API completo
2. ✅ Rotas Flask
3. ✅ Webhook handler
4. ✅ Integração com sua IA
5. ✅ Dashboard atualizado
6. ✅ Migração automática (Z-API ou whatsapp-web.js)

**É mais rápido que Twilio e funciona bem para começar!**

Me diga se quer que eu implemente Z-API agora! 🚀
