# 🔄 Como Reiniciar o Servidor Node.js Corretamente

## ⚠️ IMPORTANTE:

O servidor Node.js precisa ser **reiniciado** para aplicar as correções de verificação de conexão.

---

## 📋 PASSOS PARA REINICIAR:

### **1. Encontrar o Processo:**
```bash
lsof -ti:5001
```
Isso mostra o PID (número do processo) do servidor rodando na porta 5001.

### **2. Parar o Servidor:**

**Opção A - Se estiver em um terminal:**
- Pressione `Ctrl+C` no terminal onde o servidor está rodando

**Opção B - Se não souber qual terminal:**
```bash
# Substitua PID pelo número retornado pelo comando anterior
kill -9 PID
```

### **3. Iniciar o Servidor Novamente:**

**Opção A - Servidor na raiz:**
```bash
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

**Opção B - Servidor em web/:**
```bash
cd "/Users/air/Ylada BOT"
node web/whatsapp_server.js
```

---

## ✅ VERIFICAR SE ESTÁ FUNCIONANDO:

### **1. Verificar Status:**
```bash
curl http://localhost:5001/status
```
**Deve retornar:** `{"ready": false, "hasQr": true, "actuallyConnected": false}` (se não estiver conectado)

### **2. Verificar Rota /chats:**
```bash
curl http://localhost:5001/chats
```
**Se estiver conectado:** Retorna lista de chats
**Se não estiver:** Retorna erro "Cliente não conectado"

### **3. Testar na Interface:**
- Acesse: `http://localhost:5002/qr`
- Deve mostrar QR Code (não deve mostrar "Conectado" incorretamente)
- Escaneie o QR Code
- Aguarde alguns segundos
- Deve mostrar "Conectado com sucesso" quando realmente conectar

---

## 🔍 QUAL SERVIDOR USAR?

**Use o `whatsapp_server.js` na raiz** - ele já tem a rota `/chats` implementada.

O `web/whatsapp_server.js` também foi atualizado, mas o da raiz é o que provavelmente está sendo usado.

---

## ⚠️ SE AINDA MOSTRAR COMO CONECTADO:

1. **Pare o servidor completamente**
2. **Delete a sessão antiga:**
   ```bash
   rm -rf .wwebjs_auth
   rm -rf data/sessions/ylada_bot
   ```
3. **Inicie o servidor novamente**
4. **Acesse `/qr` e escaneie o QR Code**

---

**Depois de reiniciar, a verificação deve funcionar corretamente!** ✅

