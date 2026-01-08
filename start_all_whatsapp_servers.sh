#!/bin/bash
cd "$(dirname "$0")"

echo "🚀 Iniciando todos os servidores WhatsApp..."

# Mata processos antigos
echo "🧹 Limpando processos antigos..."
lsof -ti :5001 | xargs kill -9 2>/dev/null
lsof -ti :5002 | xargs kill -9 2>/dev/null
lsof -ti :5003 | xargs kill -9 2>/dev/null
sleep 1

# Inicia servidores
echo "📱 Iniciando servidor na porta 5001..."
PORT=5001 node whatsapp_server.js > /tmp/whatsapp_5001.log 2>&1 &
PID1=$!
echo "   PID: $PID1"

echo "📱 Iniciando servidor na porta 5002..."
PORT=5002 node whatsapp_server.js > /tmp/whatsapp_5002.log 2>&1 &
PID2=$!
echo "   PID: $PID2"

echo "📱 Iniciando servidor na porta 5003..."
PORT=5003 node whatsapp_server.js > /tmp/whatsapp_5003.log 2>&1 &
PID3=$!
echo "   PID: $PID3"

sleep 3

# Verifica status
echo ""
echo "📊 Status:"
for port in 5001 5002 5003; do
    if curl -s http://localhost:$port/health > /dev/null 2>&1; then
        echo "   ✅ Porta $port: Rodando"
    else
        echo "   ❌ Porta $port: Não está respondendo"
        echo "      Log: tail -f /tmp/whatsapp_${port}.log"
    fi
done

echo ""
echo "📝 Para ver logs:"
echo "   tail -f /tmp/whatsapp_5001.log"
echo "   tail -f /tmp/whatsapp_5002.log"
echo "   tail -f /tmp/whatsapp_5003.log"
