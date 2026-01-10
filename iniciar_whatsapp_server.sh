#!/bin/bash

echo "🚀 Iniciando Servidor WhatsApp"
echo "=============================="
echo ""

# Verifica se já está rodando
if pgrep -f "whatsapp_server.js" > /dev/null; then
    echo "⚠️  Servidor já está rodando!"
    PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "   PID: $PID"
    echo ""
    echo "   Deseja reiniciar? (s/n)"
    read -r resposta
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        echo "   🛑 Parando servidor..."
        pkill -f "whatsapp_server.js"
        sleep 3
    else
        echo "   ✅ Mantendo servidor atual"
        exit 0
    fi
fi

# Verifica se arquivo existe
if [ ! -f "whatsapp_server.js" ]; then
    echo "❌ Arquivo whatsapp_server.js não encontrado!"
    echo "   Certifique-se de estar no diretório correto"
    exit 1
fi

# Cria diretório de logs se não existir
mkdir -p logs

# Inicia servidor
echo "▶️  Iniciando servidor..."
echo "   Porta padrão: 5001"
echo "   Logs: logs/whatsapp.log"
echo ""

# Inicia em background e redireciona logs
nohup node whatsapp_server.js > logs/whatsapp.log 2>&1 &

# Aguarda um pouco
sleep 5

# Verifica se iniciou
if pgrep -f "whatsapp_server.js" > /dev/null; then
    PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "✅ Servidor iniciado com sucesso!"
    echo "   PID: $PID"
    echo ""
    
    # Testa conexão
    echo "🔍 Testando conexão..."
    sleep 2
    
    if curl -s http://localhost:5001/health > /dev/null 2>&1; then
        echo "   ✅ Servidor está respondendo!"
    else
        echo "   ⚠️  Servidor iniciou mas ainda não está respondendo"
        echo "   💡 Aguarde mais 10-15 segundos e tente novamente"
    fi
    
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo ""
    echo "1. Aguarde 15-30 segundos para o servidor inicializar completamente"
    echo "2. Recarregue a página do QR Code (F5)"
    echo "3. O QR Code deve aparecer em 30-60 segundos"
    echo ""
    echo "📊 Para ver logs em tempo real:"
    echo "   tail -f logs/whatsapp.log"
    echo ""
else
    echo "❌ Erro ao iniciar servidor!"
    echo ""
    echo "📋 Verifique:"
    echo "   1. Node.js está instalado? (node --version)"
    echo "   2. Dependências instaladas? (npm install)"
    echo "   3. Porta 5001 está livre? (lsof -i :5001)"
    echo ""
    echo "📊 Logs de erro:"
    tail -20 logs/whatsapp.log 2>/dev/null || echo "   Nenhum log disponível"
fi

