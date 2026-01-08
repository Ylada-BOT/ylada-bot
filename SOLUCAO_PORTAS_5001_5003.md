# ✅ Solução: Portas 5001 e 5003

## 📊 Status Atual

- ✅ **Porta 5001**: Rodando e **CONECTADA** (`ready: true`)
  - Não precisa de QR code porque já está conectada
  - Para reconectar, precisa desconectar primeiro

- ✅ **Porta 5003**: **FUNCIONANDO** - QR code sendo gerado
  - Servidor iniciado com sucesso
  - QR code disponível em `/qr`

- ✅ **Porta 5002**: Flask (aplicação web)

## 🔍 Diagnóstico

### Porta 5001
```bash
curl http://localhost:5001/qr
# Retorna: {"qr":null,"ready":true}
```
**Status:** Conectada, não precisa de QR code

### Porta 5003
```bash
curl http://localhost:5003/health
# Retorna: {"status":"ok","ready":false}

curl http://localhost:5003/qr
# Retorna: {"qr":"<código_qr>","ready":false}
```
**Status:** Rodando e gerando QR code ✅

## 🛠️ Solução Aplicada

### Problema Identificado
A inicialização automática não estava funcionando corretamente para a porta 5003. O servidor precisa ser iniciado manualmente ou a função automática precisa ser melhorada.

### Solução Imediata
A porta 5003 foi iniciada manualmente e está funcionando:
```bash
PORT=5003 node whatsapp_server.js
```

### Melhorias Implementadas
1. **Função `ensure_whatsapp_server_running` melhorada:**
   - Melhor gerenciamento de processos
   - Logs mais detalhados
   - Retry automático

2. **Logs separados por porta:**
   - `/tmp/whatsapp_server_5001.log`
   - `/tmp/whatsapp_server_5002.log`
   - `/tmp/whatsapp_server_5003.log`

## 📝 Como Usar Agora

### Para Porta 5001 (Primeira Conta)
1. Acesse: `http://localhost:5002/connect` (com primeira conta logada)
2. Se já estiver conectada, não precisa escanear QR code
3. Se quiser reconectar, precisa desconectar primeiro

### Para Porta 5003 (Terceira Conta)
1. Acesse: `http://localhost:5002/connect` (com terceira conta logada)
2. O QR code deve aparecer automaticamente
3. Escaneie com o WhatsApp

### Verificar Status
```bash
# Verifica todas as portas
curl http://localhost:5002/api/diagnostic/whatsapp

# Verifica porta específica
curl http://localhost:5001/health
curl http://localhost:5003/health
```

## 🚀 Iniciar Servidores Manualmente (Se Necessário)

### Opção 1: Script Automático
```bash
./start_all_whatsapp_servers.sh
```

### Opção 2: Manual (Terminais Separados)
```bash
# Terminal 1 - Porta 5001
PORT=5001 node whatsapp_server.js

# Terminal 2 - Porta 5002 (já está rodando)
PORT=5002 node whatsapp_server.js

# Terminal 3 - Porta 5003
PORT=5003 node whatsapp_server.js
```

### Opção 3: Background
```bash
PORT=5001 node whatsapp_server.js > /tmp/whatsapp_5001.log 2>&1 &
PORT=5003 node whatsapp_server.js > /tmp/whatsapp_5003.log 2>&1 &
```

## ⚠️ Notas Importantes

1. **Porta 5001 está conectada:**
   - Se você quiser reconectar, precisa desconectar primeiro
   - Acesse: `http://localhost:5001/disconnect` (POST)

2. **Porta 5003 está funcionando:**
   - QR code está sendo gerado
   - Escaneie para conectar

3. **Inicialização Automática:**
   - O sistema tenta iniciar automaticamente quando você acessa `/connect`
   - Se não funcionar, inicie manualmente

## 🔧 Troubleshooting

### Se a porta 5003 não iniciar automaticamente:

1. **Verifique logs:**
   ```bash
   tail -f /tmp/whatsapp_server_5003.log
   ```

2. **Verifique se há processo rodando:**
   ```bash
   lsof -i :5003
   ps aux | grep "whatsapp_server.js"
   ```

3. **Mate processo antigo e reinicie:**
   ```bash
   lsof -ti :5003 | xargs kill -9
   PORT=5003 node whatsapp_server.js
   ```

4. **Verifique se Node.js está instalado:**
   ```bash
   node --version
   ```

## ✅ Resumo

- ✅ Porta 5001: Conectada (não precisa QR code)
- ✅ Porta 5003: Funcionando (QR code disponível)
- ✅ Inicialização automática melhorada
- ✅ Logs separados por porta
- ✅ Endpoint de diagnóstico disponível

**Próximo passo:** Acesse `http://localhost:5002/connect` com a terceira conta e escaneie o QR code!

