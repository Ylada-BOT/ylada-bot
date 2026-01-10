#!/bin/bash

echo "🔍 DIAGNÓSTICO: Problema ao Escanear QR Code"
echo "=============================================="
echo ""

# 1. Verifica se servidor está rodando
echo "1️⃣ Verificando se servidor WhatsApp está rodando..."
if pgrep -f "whatsapp_server.js" > /dev/null; then
    echo "   ✅ Servidor WhatsApp está rodando"
    SERVER_PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "   📌 PID: $SERVER_PID"
else
    echo "   ❌ Servidor WhatsApp NÃO está rodando!"
    echo "   💡 Execute: node whatsapp_server.js"
    exit 1
fi

echo ""

# 2. Verifica portas
echo "2️⃣ Verificando portas..."
if lsof -i :5001 > /dev/null 2>&1; then
    echo "   ✅ Porta 5001 está aberta"
else
    echo "   ⚠️  Porta 5001 não está aberta (pode estar usando outra porta)"
fi

echo ""

# 3. Verifica sessões antigas
echo "3️⃣ Verificando sessões antigas..."
SESSION_COUNT=$(find . -maxdepth 1 -name ".wwebjs_auth_*" -type d 2>/dev/null | wc -l | tr -d ' ')
if [ "$SESSION_COUNT" -gt 0 ]; then
    echo "   ⚠️  Encontradas $SESSION_COUNT sessões antigas"
    echo "   💡 Isso pode causar conflitos. Deseja limpar? (s/n)"
    read -r resposta
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        echo "   🧹 Limpando sessões..."
        rm -rf .wwebjs_auth_* .wwebjs_cache_* data/sessions/* 2>/dev/null
        echo "   ✅ Sessões limpas!"
        echo "   💡 Reinicie o servidor: pkill -f whatsapp_server.js && node whatsapp_server.js"
    fi
else
    echo "   ✅ Nenhuma sessão antiga encontrada"
fi

echo ""

# 4. Verifica logs recentes
echo "4️⃣ Últimas mensagens do servidor (últimos 20 segundos):"
echo "   (Se não aparecer nada, o servidor pode estar travado)"
echo ""
timeout 2 tail -f /dev/null 2>/dev/null || true

echo ""
echo "=============================================="
echo "📋 PRÓXIMOS PASSOS:"
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
echo "   - Escaneie IMEDIATAMENTE (não espere!)"
echo ""
echo "5. Se QR Code expirar:"
echo "   - Atualize a página (F5)"
echo "   - Escaneie o novo QR Code"
echo ""

