# 🔧 Corrigir QR Code no Localhost

## ❌ Problema:

O QR Code não abre no localhost (`http://localhost:5002/qr`)

## 🔍 Possíveis Causas:

### **1. Servidor Flask não está rodando**
- Verifique se o servidor está rodando na porta 5002
- Execute: `cd web && python3 app.py`

### **2. Servidor WhatsApp Web.js não está rodando**
- O QR Code precisa do servidor Node.js na porta 5001
- Verifique se está rodando: `lsof -ti:5001`

### **3. Erro ao iniciar servidor Node.js**
- O código tenta iniciar automaticamente, mas pode falhar
- Verifique os logs do terminal onde o Flask está rodando

---

## ✅ Solução Passo a Passo:

### **Passo 1: Iniciar Servidor Flask**
```bash
cd "/Users/air/Ylada BOT/web"
python3 app.py
```

**Deve aparecer:**
```
🚀 Ylada BOT rodando em http://localhost:5002
```

### **Passo 2: Acessar Página QR**
1. Abra o navegador
2. Acesse: `http://localhost:5002/qr`
3. A página deve carregar

### **Passo 3: Verificar se Servidor Node.js Inicia**
- A página `/qr` tenta iniciar o servidor Node.js automaticamente
- Verifique o terminal do Flask - deve aparecer:
  ```
  [*] Iniciando servidor WhatsApp Web.js ao acessar /qr...
  ```

### **Passo 4: Se Não Iniciar Automaticamente**
Execute manualmente:
```bash
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

Ou use o script:
```bash
cd "/Users/air/Ylada BOT"
./iniciar_whatsapp.sh
```

---

## 🔍 Verificar se Está Funcionando:

### **1. Verificar Servidor Flask:**
```bash
curl http://localhost:5002/health
```
**Deve retornar:** `{"status": "ok", "bot": "Ylada BOT"}`

### **2. Verificar Servidor WhatsApp:**
```bash
curl http://localhost:5001/health
```
**Deve retornar:** `{"status": "ok", "ready": false}`

### **3. Verificar QR Code API:**
```bash
curl http://localhost:5002/api/qr
```
**Deve retornar:** JSON com `qr` ou mensagem de erro

---

## ⚠️ Problemas Comuns:

### **Erro: "Cannot GET /qr"**
- Servidor Flask não está rodando
- Inicie: `cd web && python3 app.py`

### **Erro: "Connection refused" na porta 5001**
- Servidor Node.js não está rodando
- O código tenta iniciar automaticamente, mas pode falhar
- Inicie manualmente: `node whatsapp_server.js`

### **QR Code não aparece (fica "Aguardando...")**
- Servidor Node.js pode estar iniciando (aguarde 10-15 segundos)
- Verifique os logs do terminal
- Tente clicar em "Reiniciar Servidor" na página

### **Erro: "Module not found"**
- Instale dependências: `pip install -r requirements.txt`
- Instale dependências Node.js: `npm install`

---

## 🎯 Teste Completo:

1. ✅ Servidor Flask rodando na porta 5002
2. ✅ Acessar `http://localhost:5002/qr`
3. ✅ Página carrega sem erros
4. ✅ Servidor Node.js inicia automaticamente (ou manualmente)
5. ✅ QR Code aparece na página após 5-10 segundos
6. ✅ QR Code também aparece no terminal (ASCII)

**Se todos os passos funcionarem, o QR Code está funcionando!** ✅

