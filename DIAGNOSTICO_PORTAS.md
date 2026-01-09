# 🔍 Diagnóstico: Portas 5001 e 5003 não funcionam

## ❌ Problema Identificado

- ✅ Porta 5002: Funcionando (segunda conta)
- ❌ Porta 5001: Não funciona (primeira conta)
- ❌ Porta 5003: Não funciona (terceira conta)

## 🔍 Diagnóstico

### Verificar processos rodando

```bash
# Verifica processos nas portas
lsof -i :5001
lsof -i :5002
lsof -i :5003

# Verifica processos Node.js
ps aux | grep "whatsapp_server.js"
```

### Verificar se servidores respondem

```bash
# Testa porta 5001
curl http://localhost:5001/health

# Testa porta 5002
curl http://localhost:5002/health

# Testa porta 5003
curl http://localhost:5003/health
```

### Endpoint de Diagnóstico

Acesse: `http://localhost:5002/api/diagnostic/whatsapp`

Este endpoint verifica o status de todas as portas (5001-5010) e retorna:
- Status de cada porta
- Se há processo rodando
- Se o servidor responde
- Se tem QR code disponível

## 🛠️ Soluções

### Solução 1: Iniciar servidores manualmente

```bash
# Terminal 1 - Porta 5001
PORT=5001 node whatsapp_server.js

# Terminal 2 - Porta 5002 (já está funcionando)
PORT=5002 node whatsapp_server.js

# Terminal 3 - Porta 5003
PORT=5003 node whatsapp_server.js
```

### Solução 2: Usar script de inicialização

Crie um script `start_all_servers.sh`:

```bash
#!/bin/bash
cd "$(dirname "$0")"

# Mata processos antigos
lsof -ti :5001 | xargs kill -9 2>/dev/null
lsof -ti :5002 | xargs kill -9 2>/dev/null
lsof -ti :5003 | xargs kill -9 2>/dev/null

# Inicia servidores
PORT=5001 node whatsapp_server.js > /tmp/whatsapp_5001.log 2>&1 &
PORT=5002 node whatsapp_server.js > /tmp/whatsapp_5002.log 2>&1 &
PORT=5003 node whatsapp_server.js > /tmp/whatsapp_5003.log 2>&1 &

echo "Servidores iniciados. Verifique os logs:"
echo "  tail -f /tmp/whatsapp_5001.log"
echo "  tail -f /tmp/whatsapp_5002.log"
echo "  tail -f /tmp/whatsapp_5003.log"
```

### Solução 3: Verificar logs

```bash
# Ver logs do Flask (pode mostrar erros de inicialização)
tail -f /tmp/flask_app.log

# Ver logs de cada servidor
tail -f /tmp/whatsapp_server_5001.log
tail -f /tmp/whatsapp_server_5002.log
tail -f /tmp/whatsapp_server_5003.log
```

## 🔧 Melhorias Implementadas

1. **Função `ensure_whatsapp_server_running` melhorada:**
   - Mais logs de diagnóstico
   - Retry automático (3 tentativas)
   - Logs salvos em arquivos separados por porta
   - Verificação melhorada de processos

2. **Endpoint de diagnóstico:**
   - `/api/diagnostic/whatsapp` - Verifica status de todas as portas

3. **Tratamento de erros melhorado:**
   - Tenta reiniciar servidor automaticamente em caso de erro
   - Mensagens de erro mais informativas

## 📝 Próximos Passos

1. Acesse o endpoint de diagnóstico: `http://localhost:5002/api/diagnostic/whatsapp`
2. Verifique quais portas estão realmente rodando
3. Se necessário, inicie os servidores manualmente
4. Verifique os logs para identificar erros

## ⚠️ Possíveis Causas

1. **Processos morrendo após iniciar:**
   - Verifique erros nos logs
   - Pode ser problema de permissões
   - Pode ser problema com Node.js

2. **Porta já em uso:**
   - Verifique se outra aplicação está usando a porta
   - Mate processos antigos: `lsof -ti :5001 | xargs kill -9`

3. **Problema com inicialização automática:**
   - O processo pode não estar persistindo
   - Tente iniciar manualmente primeiro


