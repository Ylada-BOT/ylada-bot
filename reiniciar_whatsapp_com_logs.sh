#!/bin/bash

echo "🔄 Reiniciando Servidor WhatsApp com Logs"
echo "=========================================="
echo ""

# Para servidor
echo "1️⃣ Parando servidor..."
pkill -f "whatsapp_server.js"
sleep 3

# Limpa sessões (opcional - descomente se necessário)
# echo "2️⃣ Limpando sessões..."
# rm -rf .wwebjs_auth_* .wwebjs_cache_* 2>/dev/null

# Cria diretório de logs
mkdir -p logs

# Inicia servidor com logs
echo "3️⃣ Iniciando servidor com logs..."
echo "   Logs serão salvos em: logs/whatsapp.log"
echo "   Para ver logs em tempo real: tail -f logs/whatsapp.log"
echo ""

nohup node whatsapp_server.js > logs/whatsapp.log 2>&1 &

sleep 5

# Verifica se iniciou
if pgrep -f "whatsapp_server.js" > /dev/null; then
    PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "✅ Servidor iniciado (PID: $PID)"
    echo ""
    echo "📊 Para ver logs em tempo real:"
    echo "   tail -f logs/whatsapp.log"
    echo ""
    echo "🔍 Para procurar por eventos de conexão:"
    echo "   grep -i 'connecting\\|authenticated\\|ready' logs/whatsapp.log"
else
    echo "❌ Erro ao iniciar servidor!"
    echo "📊 Verifique logs:"
    tail -20 logs/whatsapp.log 2>/dev/null || echo "   Nenhum log disponível"
fi

