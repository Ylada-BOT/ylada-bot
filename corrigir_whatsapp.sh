#!/bin/bash

echo "🔧 CORREÇÃO: Integração WhatsApp"
echo "================================"
echo ""

# 1. Para processos antigos
echo "[1/6] Parando processos antigos..."
pkill -f "node whatsapp_server.js" 2>/dev/null
pkill -f "python.*app.py" 2>/dev/null
sleep 2

# 2. Limpa sessões antigas
echo "[2/6] Limpando sessões antigas..."
rm -rf .wwebjs_auth 2>/dev/null
rm -rf .wwebjs_cache 2>/dev/null
rm -rf data/sessions/ylada_bot 2>/dev/null
echo "✅ Sessões limpas"

# 3. Verifica Node.js
echo "[3/6] Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado!"
    echo "   Instale: https://nodejs.org"
    exit 1
fi
echo "✅ Node.js: $(node --version)"

# 4. Verifica dependências
echo "[4/6] Verificando dependências..."
if [ ! -d "node_modules/whatsapp-web.js" ]; then
    echo "   Instalando dependências..."
    npm install whatsapp-web.js qrcode-terminal express 2>&1 | tail -3
fi
echo "✅ Dependências OK"

# 5. Inicia servidor Node.js
echo "[5/6] Iniciando servidor WhatsApp..."
cd "$(dirname "$0")"
node whatsapp_server.js > whatsapp_server.log 2>&1 &
NODE_PID=$!
sleep 5

# Verifica se iniciou
if ps -p $NODE_PID > /dev/null; then
    echo "✅ Servidor Node.js iniciado (PID: $NODE_PID)"
else
    echo "❌ Erro ao iniciar servidor Node.js"
    echo "   Verifique: cat whatsapp_server.log"
    exit 1
fi

# 6. Verifica se está respondendo
echo "[6/6] Verificando servidor..."
sleep 3
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ Servidor respondendo!"
    echo ""
    echo "📱 PRÓXIMOS PASSOS:"
    echo "   1. Acesse: http://localhost:5002/qr"
    echo "   2. Escaneie o QR Code com seu WhatsApp"
    echo "   3. Aguarde confirmação de conexão"
    echo ""
    echo "📋 LOGS:"
    echo "   tail -f whatsapp_server.log"
else
    echo "❌ Servidor não está respondendo"
    echo "   Verifique: cat whatsapp_server.log"
    exit 1
fi





