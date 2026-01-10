# 🔧 Solução: Erro 503 mesmo com Servidor Rodando

## ⚠️ PROBLEMA

O servidor WhatsApp **ESTÁ rodando** e gerando QR Code corretamente, mas o Flask retorna **erro 503** ao tentar acessar.

**Sintomas:**
- ✅ Servidor Node.js está rodando (`ps aux | grep whatsapp_server`)
- ✅ Servidor responde no `/health` (`curl http://localhost:5001/health`)
- ✅ Servidor gera QR Code (`curl http://localhost:5001/qr`)
- ❌ Flask retorna erro 503 ao acessar `/api/qr`

---

## 🔍 CAUSA

O problema geralmente é:

1. **Timeout muito curto** - Flask tenta acessar mas timeout antes do servidor responder
2. **URL incorreta** - Flask está tentando acessar URL errada (produção vs desenvolvimento)
3. **Problema de importação** - `http_client` não está sendo importado corretamente
4. **Servidor lento** - Servidor demora mais de 30s para gerar QR Code

---

## ✅ SOLUÇÃO RÁPIDA

### **1. Verificar se Servidor Está Rodando**

```bash
# Verifica processos
ps aux | grep whatsapp_server

# Testa conexão direta
curl http://localhost:5001/health
curl http://localhost:5001/qr?user_id=1
```

**Se funcionar:** Servidor está OK, problema é no Flask  
**Se não funcionar:** Inicie o servidor primeiro

---

### **2. Reiniciar Servidor Flask**

O Flask pode ter cache ou estado antigo. Reinicie:

```bash
# Para Flask
pkill -f "python.*app.py\|flask\|gunicorn"

# Reinicia Flask
python3 web/app.py
```

---

### **3. Verificar Logs do Flask**

Procure por erros nos logs:

```bash
# Se Flask está rodando, veja logs
tail -f logs/app.log

# Ou no terminal onde Flask está rodando
```

**Procure por:**
- `Erro de conexão/timeout`
- `Todas as tentativas falharam`
- `URL tentada:`

---

### **4. Aumentar Timeout (Já Foi Feito)**

O timeout já foi aumentado para 30 segundos. Se ainda não funcionar:

1. **Recarregue a página** (F5)
2. **Aguarde 30-60 segundos** para QR Code aparecer
3. **Verifique console do navegador** (F12) para erros

---

### **5. Verificar Configuração**

Verifique se `.env` está correto:

```bash
cat .env | grep WHATSAPP
```

**Deve ter:**
```
WHATSAPP_SERVER_URL=http://localhost:5001
WHATSAPP_SERVER_PORT=5001
```

**Se estiver em produção:**
```
WHATSAPP_SERVER_URL=https://seu-servidor.railway.app
```

---

## 🐛 DEBUG DETALHADO

### **Teste 1: Servidor Node.js**

```bash
# Testa health
curl http://localhost:5001/health

# Testa QR Code
curl http://localhost:5001/qr?user_id=1
```

**Esperado:** Ambos devem retornar JSON válido

---

### **Teste 2: Flask Acessando Servidor**

No terminal do Flask, você deve ver logs como:

```
Buscando QR Code do servidor WhatsApp em http://localhost:5001 para user_id=1_1
Tentativa 1/3: GET http://localhost:5001/qr?user_id=1_1
✓ Sucesso: 200
```

**Se ver erros:**
- `ConnectionError` → Servidor não está acessível
- `Timeout` → Servidor está muito lento
- `Todas as tentativas falharam` → Verifique URL

---

### **Teste 3: Console do Navegador**

1. Abra página de QR Code
2. Pressione **F12** (DevTools)
3. Vá em **Console**
4. Procure por erros

**Erros comuns:**
- `503 Service Unavailable` → Flask não conseguiu acessar servidor
- `Failed to fetch` → Problema de rede
- `Timeout` → Servidor demorou muito

---

## 🔄 SOLUÇÃO COMPLETA

Se nada funcionar, execute:

```bash
# 1. Para tudo
pkill -f "whatsapp_server.js"
pkill -f "python.*app.py\|flask"

# 2. Limpa sessões
rm -rf .wwebjs_auth_* .wwebjs_cache_*

# 3. Aguarda
sleep 5

# 4. Inicia servidor WhatsApp
node whatsapp_server.js &

# 5. Aguarda servidor iniciar
sleep 10

# 6. Testa servidor
curl http://localhost:5001/health

# 7. Se servidor OK, inicia Flask
python3 web/app.py
```

---

## 📋 CHECKLIST

Antes de reportar problema, verifique:

- [ ] Servidor Node.js está rodando (`ps aux | grep whatsapp_server`)
- [ ] Servidor responde no `/health` (`curl http://localhost:5001/health`)
- [ ] Servidor gera QR Code (`curl http://localhost:5001/qr?user_id=1`)
- [ ] Flask está rodando (`ps aux | grep python.*app`)
- [ ] `.env` tem `WHATSAPP_SERVER_URL=http://localhost:5001`
- [ ] Recarreguei a página (F5)
- [ ] Aguardei 30-60 segundos
- [ ] Verifiquei logs do Flask
- [ ] Verifiquei console do navegador (F12)

---

## 💡 DICAS

1. **Servidor pode estar lento:** Aguarde até 60 segundos na primeira vez
2. **Cache do navegador:** Limpe cache (Ctrl+Shift+Del) ou use modo incógnito
3. **Múltiplos processos:** Verifique se não há processos duplicados
4. **Porta ocupada:** Verifique se porta 5001 está livre (`lsof -i :5001`)

---

**Última atualização:** 2025-01-27

