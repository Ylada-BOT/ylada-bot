# 🧪 Guia de Teste - Rate Limiting e Fila de Mensagens

**Data:** 2025-01-27  
**Modo:** Desenvolvimento → Produção

---

## 📋 PRÉ-REQUISITOS

### **1. Verificar Ambiente**
- ✅ Python 3.8+ instalado
- ✅ Node.js instalado (para WhatsApp server)
- ✅ PostgreSQL/Supabase configurado
- ⚠️ Redis (opcional, mas recomendado)

### **2. Instalar Dependências**
```bash
cd "/Users/air/Ylada BOT"
pip install -r requirements.txt
```

**Dependências novas:**
- `flask-limiter==3.5.0`
- `redis==5.0.1`
- `huey==2.5.0`

---

## 🧪 TESTE 1: Verificar Instalação

### **Passo 1.1: Verificar Imports**
```bash
python3 -c "
from web.utils.rate_limiter import init_rate_limiter, rate_limit_whatsapp
from web.utils.message_queue import init_message_queue, get_message_queue
from web.workers.message_worker import init_message_worker
print('✅ Todos os imports funcionaram!')
"
```

**Resultado esperado:**
```
✅ Todos os imports funcionaram!
```

**Se der erro:**
```bash
pip install flask-limiter redis huey
```

---

## 🧪 TESTE 2: Rate Limiting (Modo Desenvolvimento)

### **Passo 2.1: Iniciar Servidor Flask**
```bash
cd "/Users/air/Ylada BOT"
python3 web/app.py
```

**Resultado esperado:**
```
✅ Rate limiter configurado com memória (use Redis para produção)
✅ Fila de mensagens configurada com memória (não persistente)
✅ Worker de mensagens iniciado em background
```

### **Passo 2.2: Testar Rate Limiting**

**Em outro terminal, execute:**
```bash
# Teste 1: Enviar 1 requisição (deve funcionar)
curl -X POST http://localhost:5002/webhook \
  -H "Content-Type: application/json" \
  -d '{"from": "5511999999999", "body": "teste"}'

# Teste 2: Enviar 20 requisições rapidamente (deve limitar)
for i in {1..20}; do
  curl -X POST http://localhost:5002/webhook \
    -H "Content-Type: application/json" \
    -d "{\"from\": \"5511999999999\", \"body\": \"teste $i\"}" &
done
wait
```

**Resultado esperado:**
- Primeiras 15 requisições: ✅ Sucesso
- Requisições 16-20: ❌ Erro 429 (Too Many Requests)

**Verificar logs:**
```
[INFO] Rate limit exceeded for key: ...
```

---

## 🧪 TESTE 3: Fila de Mensagens (Modo Desenvolvimento)

### **Passo 3.1: Verificar Worker**

**No terminal do Flask, você deve ver:**
```
[✓] Worker de mensagens iniciado em background
```

### **Passo 3.2: Adicionar Mensagem à Fila**

**Criar script de teste:**
```python
# test_queue.py
from web.utils.message_queue import init_message_queue, get_message_queue
from web.workers.message_worker import init_message_worker
from web.app import whatsapp

# Inicializa fila
queue = init_message_queue(use_redis=False)
print(f"✅ Fila inicializada. Tamanho: {queue.get_queue_size()}")

# Adiciona mensagem
message_id = queue.add_message(
    phone="5511999999999",
    message="Teste de fila",
    priority=1
)
print(f"✅ Mensagem adicionada: {message_id}")
print(f"📊 Tamanho da fila: {queue.get_queue_size()}")

# Inicia worker (se WhatsApp estiver conectado)
if whatsapp and whatsapp.is_ready():
    worker = init_message_worker(queue, whatsapp, interval=1.0)
    print("✅ Worker iniciado")
    print("⏳ Aguardando processamento...")
    import time
    time.sleep(5)
    
    # Verifica status
    stats = worker.get_stats()
    print(f"📊 Estatísticas:")
    print(f"   - Processadas: {stats['processed']}")
    print(f"   - Falhadas: {stats['failed']}")
    print(f"   - Fila: {stats['queue_size']}")
else:
    print("⚠️ WhatsApp não está conectado. Conecte primeiro.")
```

**Executar:**
```bash
python3 test_queue.py
```

**Resultado esperado:**
```
✅ Fila inicializada. Tamanho: 0
✅ Mensagem adicionada: msg_1234567890_5511999999999
📊 Tamanho da fila: 1
✅ Worker iniciado
⏳ Aguardando processamento...
📤 Processando mensagem msg_1234567890_5511999999999 para 5511999999999
✅ Mensagem msg_1234567890_5511999999999 enviada com sucesso
📊 Estatísticas:
   - Processadas: 1
   - Falhadas: 0
   - Fila: 0
```

---

## 🧪 TESTE 4: Integração Completa

### **Passo 4.1: Testar Webhook com Fila**

**1. Conectar WhatsApp:**
- Acesse: `http://localhost:5002/qr`
- Escaneie QR Code
- Aguarde conectar

**2. Enviar mensagem para o bot:**
- Envie uma mensagem do seu WhatsApp para o número conectado
- Exemplo: "Olá"

**3. Verificar logs:**
```
[📨] Mensagem recebida de 5511999999999: Olá
[🤖] Resposta da IA: Olá! Como posso ajudar?
[✓] Resposta adicionada à fila para 5511999999999
📤 Processando mensagem msg_... para 5511999999999
✅ Mensagem msg_... enviada com sucesso
```

**4. Verificar se mensagem foi recebida:**
- Verifique seu WhatsApp
- Deve receber resposta do bot

---

## 🧪 TESTE 5: Retry Automático

### **Passo 5.1: Simular Falha**

**1. Desconectar WhatsApp temporariamente:**
```bash
curl -X POST http://localhost:5002/api/whatsapp-disconnect
```

**2. Adicionar mensagem à fila:**
```python
# test_retry.py
from web.utils.message_queue import get_message_queue

queue = get_message_queue()
message_id = queue.add_message(
    phone="5511999999999",
    message="Teste de retry",
    max_retries=3,
    retry_delay=5
)
print(f"✅ Mensagem adicionada: {message_id}")
print("⏳ Aguardando retry...")
```

**3. Reconectar WhatsApp:**
- Acesse: `http://localhost:5002/qr`
- Escaneie QR Code novamente

**4. Verificar logs:**
```
⚠️ WhatsApp não está conectado
🔄 Mensagem msg_... agendada para retry (tentativa 1/3)
🔄 Mensagem msg_... agendada para retry (tentativa 2/3)
✅ Mensagem msg_... enviada com sucesso
```

---

## 🚀 TESTE 6: Modo Produção (Com Redis)

### **Passo 6.1: Instalar Redis**

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Verificar:**
```bash
redis-cli ping
# Deve retornar: PONG
```

### **Passo 6.2: Configurar .env.local**

```env
USE_REDIS=true
REDIS_URL=redis://localhost:6379/0
```

### **Passo 6.3: Reiniciar Servidor**

```bash
python3 web/app.py
```

**Resultado esperado:**
```
✅ Rate limiter configurado com Redis
✅ Fila de mensagens configurada com Redis
✅ Worker de mensagens iniciado em background
```

### **Passo 6.4: Testar Persistência**

**1. Adicionar mensagens à fila:**
```python
from web.utils.message_queue import get_message_queue

queue = get_message_queue()
for i in range(5):
    queue.add_message(
        phone=f"551199999{i:06d}",
        message=f"Mensagem {i}",
        priority=i
    )
print(f"✅ 5 mensagens adicionadas. Fila: {queue.get_queue_size()}")
```

**2. Reiniciar servidor:**
```bash
# Parar servidor (Ctrl+C)
python3 web/app.py
```

**3. Verificar se mensagens persistiram:**
```python
from web.utils.message_queue import get_message_queue

queue = get_message_queue()
print(f"📊 Tamanho da fila após reiniciar: {queue.get_queue_size()}")
# Deve mostrar 5 (ou menos se já processadas)
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

### **Rate Limiting:**
- [ ] Imports funcionam
- [ ] Limite de 15 msg/min funciona
- [ ] Erro 429 quando excede limite
- [ ] Logs mostram rate limiting

### **Fila de Mensagens:**
- [ ] Fila inicializa corretamente
- [ ] Mensagens são adicionadas à fila
- [ ] Worker processa mensagens
- [ ] Mensagens são enviadas via WhatsApp
- [ ] Estatísticas funcionam

### **Retry Automático:**
- [ ] Retry em caso de falha
- [ ] Delay entre tentativas funciona
- [ ] Máximo de tentativas respeitado
- [ ] Mensagens falhadas são marcadas

### **Integração:**
- [ ] Webhook usa fila automaticamente
- [ ] Respostas da IA vão para fila
- [ ] Worker processa em background
- [ ] Logs mostram fluxo completo

### **Produção (Redis):**
- [ ] Redis conecta corretamente
- [ ] Fila persiste entre reinicializações
- [ ] Rate limiting usa Redis
- [ ] Performance melhorada

---

## 🐛 TROUBLESHOOTING

### **Erro: ModuleNotFoundError**
```bash
pip install flask-limiter redis huey
```

### **Erro: Redis não conecta**
- Verifique se Redis está rodando: `redis-cli ping`
- Verifique URL no `.env.local`
- Sistema faz fallback para memória automaticamente

### **Worker não processa mensagens**
- Verifique se WhatsApp está conectado
- Verifique logs do worker
- Verifique se thread está rodando

### **Rate limiting não funciona**
- Verifique se `init_rate_limiter()` foi chamado
- Verifique logs
- Teste com curl para verificar

### **Mensagens não persistem**
- Verifique se Redis está configurado
- Verifique se `USE_REDIS=true`
- Memória não persiste (normal)

---

## 📊 MÉTRICAS DE SUCESSO

### **Rate Limiting:**
- ✅ Limita corretamente (15/min)
- ✅ Retorna 429 quando excede
- ✅ Logs mostram bloqueios

### **Fila de Mensagens:**
- ✅ Mensagens são adicionadas
- ✅ Worker processa automaticamente
- ✅ Taxa de sucesso > 95%
- ✅ Retry funciona

### **Performance:**
- ✅ Latência < 2 segundos (envio)
- ✅ Worker processa sem travamentos
- ✅ Fila não cresce indefinidamente

---

## 🎯 PRÓXIMOS PASSOS APÓS TESTES

1. ✅ Validar que tudo funciona
2. ⏳ Corrigir problemas encontrados
3. ⏳ Otimizar performance
4. ⏳ Adicionar monitoramento
5. ⏳ Continuar com builder visual

---

**Última atualização:** 2025-01-27



