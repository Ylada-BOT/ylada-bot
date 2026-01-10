#!/bin/bash

echo "🔍 DIAGNÓSTICO COMPLETO: Problema QR Code"
echo "=========================================="
echo ""

# 1. Verifica se servidor Node.js está rodando
echo "1️⃣ Verificando servidor WhatsApp (Node.js)..."
if pgrep -f "whatsapp_server.js" > /dev/null; then
    SERVER_PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "   ✅ Servidor está rodando (PID: $SERVER_PID)"
    
    # Verifica porta
    PORT=$(lsof -p $SERVER_PID -iTCP -sTCP:LISTEN | grep -oP ':\K[0-9]+' | head -1)
    if [ -n "$PORT" ]; then
        echo "   ✅ Porta: $PORT"
    else
        echo "   ⚠️  Não conseguiu detectar a porta"
    fi
else
    echo "   ❌ Servidor NÃO está rodando!"
    echo "   💡 Execute: node whatsapp_server.js"
    exit 1
fi

echo ""

# 2. Testa conexão com servidor
echo "2️⃣ Testando conexão com servidor..."
if [ -n "$PORT" ]; then
    if curl -s "http://localhost:$PORT/health" > /dev/null 2>&1; then
        echo "   ✅ Servidor responde no /health"
    else
        echo "   ❌ Servidor NÃO responde no /health"
    fi
    
    # Tenta buscar QR Code
    QR_RESPONSE=$(curl -s "http://localhost:$PORT/qr" 2>&1)
    if echo "$QR_RESPONSE" | grep -q "qr\|ready\|generating"; then
        echo "   ✅ Endpoint /qr está respondendo"
        echo "   📋 Resposta: $(echo "$QR_RESPONSE" | head -c 100)..."
    else
        echo "   ❌ Endpoint /qr NÃO está respondendo corretamente"
        echo "   📋 Resposta: $QR_RESPONSE"
    fi
else
    echo "   ⚠️  Não foi possível testar (porta não detectada)"
fi

echo ""

# 3. Verifica sessões antigas
echo "3️⃣ Verificando sessões antigas..."
SESSION_COUNT=$(find . -maxdepth 1 -name ".wwebjs_auth_*" -type d 2>/dev/null | wc -l | tr -d ' ')
CACHE_COUNT=$(find . -maxdepth 1 -name ".wwebjs_cache_*" -type d 2>/dev/null | wc -l | tr -d ' ')

if [ "$SESSION_COUNT" -gt 0 ] || [ "$CACHE_COUNT" -gt 0 ]; then
    echo "   ⚠️  Encontradas $SESSION_COUNT sessões e $CACHE_COUNT caches"
    echo "   💡 Isso pode causar conflitos"
    echo ""
    echo "   Deseja limpar TODAS as sessões? (s/n)"
    read -r resposta
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        echo "   🧹 Limpando sessões..."
        pkill -f "whatsapp_server.js"
        sleep 2
        rm -rf .wwebjs_auth_* .wwebjs_cache_* data/sessions/* 2>/dev/null
        echo "   ✅ Sessões limpas!"
        echo "   💡 Reinicie o servidor: node whatsapp_server.js"
    fi
else
    echo "   ✅ Nenhuma sessão antiga encontrada"
fi

echo ""

# 4. Verifica logs recentes
echo "4️⃣ Últimas linhas do log do servidor:"
echo "   (Procure por erros ou mensagens de QR Code)"
echo ""
if pgrep -f "whatsapp_server.js" > /dev/null; then
    echo "   💡 Para ver logs em tempo real, execute em outro terminal:"
    echo "      tail -f /proc/$SERVER_PID/fd/1 2>/dev/null || echo 'Logs não disponíveis'"
else
    echo "   ⚠️  Servidor não está rodando, não há logs"
fi

echo ""

# 5. Verifica variáveis de ambiente
echo "5️⃣ Verificando configurações..."
if [ -f ".env" ]; then
    echo "   ✅ Arquivo .env encontrado"
    if grep -q "WHATSAPP_SERVER_URL" .env; then
        WHATSAPP_URL=$(grep "WHATSAPP_SERVER_URL" .env | cut -d '=' -f2)
        echo "   📌 WHATSAPP_SERVER_URL: $WHATSAPP_URL"
    else
        echo "   ⚠️  WHATSAPP_SERVER_URL não encontrado no .env"
    fi
    
    if grep -q "WHATSAPP_SERVER_PORT" .env; then
        WHATSAPP_PORT=$(grep "WHATSAPP_SERVER_PORT" .env | cut -d '=' -f2)
        echo "   📌 WHATSAPP_SERVER_PORT: $WHATSAPP_PORT"
    else
        echo "   ⚠️  WHATSAPP_SERVER_PORT não encontrado no .env"
    fi
else
    echo "   ⚠️  Arquivo .env não encontrado"
fi

echo ""

# 6. Verifica se Flask está rodando
echo "6️⃣ Verificando servidor Flask..."
if pgrep -f "python.*app.py\|flask\|gunicorn" > /dev/null; then
    FLASK_PID=$(pgrep -f "python.*app.py\|flask\|gunicorn" | head -1)
    echo "   ✅ Flask está rodando (PID: $FLASK_PID)"
    
    # Testa endpoint
    if curl -s "http://localhost:5002/api/qr" > /dev/null 2>&1; then
        echo "   ✅ Endpoint /api/qr está acessível"
    else
        echo "   ❌ Endpoint /api/qr NÃO está acessível"
    fi
else
    echo "   ⚠️  Flask não está rodando"
fi

echo ""

# 7. Recomendações
echo "=========================================="
echo "📋 RECOMENDAÇÕES:"
echo ""
echo "1. Se servidor não está rodando:"
echo "   node whatsapp_server.js"
echo ""
echo "2. Se há sessões antigas:"
echo "   ./limpar_sessao_whatsapp.sh"
echo ""
echo "3. No celular:"
echo "   - WhatsApp > Configurações > Aparelhos conectados"
echo "   - Desconecte TODOS os aparelhos"
echo "   - Aguarde 1 minuto"
echo ""
echo "4. Na plataforma:"
echo "   - Acesse página de QR Code"
echo "   - Aguarde QR Code aparecer (15-30 segundos)"
echo "   - Escaneie IMEDIATAMENTE"
echo ""
echo "5. Se ainda não funcionar:"
echo "   - Verifique logs do servidor Node.js"
echo "   - Verifique console do navegador (F12)"
echo "   - Tente com outro número de WhatsApp"
echo ""

