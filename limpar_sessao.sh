#!/bin/bash
echo "🧹 Limpando sessões antigas do WhatsApp..."

# Para servidor Node.js se estiver rodando
echo "⏹️  Parando servidor..."
pkill -f "node whatsapp_server.js" 2>/dev/null
sleep 2

# Remove sessões antigas
echo "🗑️  Removendo sessões..."
rm -rf data/sessions/* 2>/dev/null
rm -rf .wwebjs_auth 2>/dev/null
rm -rf .wwebjs_cache 2>/dev/null

echo "✅ Sessões limpas com sucesso!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. No WhatsApp do celular:"
echo "   - Vá em Configurações > Aparelhos conectados"
echo "   - Desconecte dispositivos antigos (deixe só 1-2)"
echo ""
echo "2. Inicie o servidor:"
echo "   node whatsapp_server.js"
echo ""
echo "3. Acesse: http://localhost:5002/qr"
echo "4. Escaneie o QR Code rapidamente"





