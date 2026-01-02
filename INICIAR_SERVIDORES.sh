#!/bin/bash
# Script para iniciar servidores do BOT YLADA

cd "$(dirname "$0")"

echo "🚀 Iniciando servidores do BOT YLADA..."
echo ""

# Verifica se venv existe
if [ ! -d "venv" ]; then
    echo "⚠️ Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask-cors requests python-dotenv flask-limiter sqlalchemy psycopg2-binary 2>&1 | tail -5
    echo "✅ Ambiente virtual criado"
else
    source venv/bin/activate
fi

# Mata processos antigos
echo "🧹 Limpando processos antigos..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:5002 | xargs kill -9 2>/dev/null
sleep 1

# Inicia WhatsApp server
echo "📱 Iniciando servidor WhatsApp (porta 5001)..."
node whatsapp_server.js > /tmp/whatsapp_server.log 2>&1 &
WHATSAPP_PID=$!
echo "   PID: $WHATSAPP_PID"
sleep 2

# Inicia Flask
echo "🌐 Iniciando servidor Flask (porta 5002)..."
python web/app.py > /tmp/flask_app.log 2>&1 &
FLASK_PID=$!
echo "   PID: $FLASK_PID"
sleep 4

# Verifica se estão rodando
echo ""
echo "📊 Status:"
if ps -p $WHATSAPP_PID > /dev/null 2>&1; then
    echo "   ✅ WhatsApp server: Rodando (PID: $WHATSAPP_PID)"
else
    echo "   ❌ WhatsApp server: Parou"
    echo "   📝 Log: tail -f /tmp/whatsapp_server.log"
fi

if ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "   ✅ Flask: Rodando (PID: $FLASK_PID)"
    curl -s http://localhost:5002/health > /dev/null 2>&1 && echo "   ✅ Flask respondendo" || echo "   ⚠️ Flask não está respondendo ainda"
else
    echo "   ❌ Flask: Parou"
    echo "   📝 Log: tail -f /tmp/flask_app.log"
    echo ""
    echo "   Últimas linhas do log:"
    tail -20 /tmp/flask_app.log
fi

echo ""
echo "🌐 Acesse: http://localhost:5002"
echo "📱 QR Code: http://localhost:5002/qr"
echo ""
echo "Para parar os servidores:"
echo "   kill $WHATSAPP_PID $FLASK_PID"



