#!/bin/bash

echo "🧹 Limpando e Reiniciando WhatsApp Server"
echo "========================================="
echo ""

# 1. Para TODOS os processos
echo "1️⃣ Parando processos..."
pkill -9 -f "whatsapp_server.js" 2>/dev/null
sleep 3

# Verifica se parou
if pgrep -f "whatsapp_server.js" > /dev/null; then
    echo "   ⚠️  Ainda há processos rodando, forçando..."
    pkill -9 -f "node.*whatsapp" 2>/dev/null
    sleep 2
fi

echo "   ✅ Processos parados"
echo ""

# 2. Limpa sessões
echo "2️⃣ Limpando sessões antigas..."
rm -rf .wwebjs_auth_* 2>/dev/null
rm -rf .wwebjs_cache_* 2>/dev/null
rm -rf data/sessions/* 2>/dev/null
echo "   ✅ Sessões limpas"
echo ""

# 3. Aguarda
echo "3️⃣ Aguardando 10 segundos..."
sleep 10
echo ""

# 4. Reinicia
echo "4️⃣ Reiniciando servidor..."
echo "   💡 O servidor vai iniciar em background"
echo "   💡 Para ver logs, execute: tail -f logs/whatsapp.log"
echo ""

# Inicia em background e redireciona logs
nohup node whatsapp_server.js > logs/whatsapp.log 2>&1 &

# Aguarda um pouco para verificar se iniciou
sleep 5

# Verifica se iniciou
if pgrep -f "whatsapp_server.js" > /dev/null; then
    PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "   ✅ Servidor iniciado (PID: $PID)"
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo ""
    echo "1. No celular:"
    echo "   - WhatsApp > Configurações > Aparelhos conectados"
    echo "   - Desconecte TODOS os aparelhos"
    echo "   - Aguarde 1 minuto"
    echo ""
    echo "2. Na plataforma:"
    echo "   - Acesse página de QR Code"
    echo "   - Aguarde 30-60 segundos para QR Code aparecer"
    echo "   - Escaneie IMEDIATAMENTE quando aparecer"
    echo ""
    echo "3. Se ainda não funcionar:"
    echo "   - Verifique logs: tail -f logs/whatsapp.log"
    echo "   - Aguarde mais tempo (servidor pode estar lento)"
    echo ""
else
    echo "   ❌ Servidor NÃO iniciou!"
    echo "   💡 Tente iniciar manualmente: node whatsapp_server.js"
    echo ""
fi

