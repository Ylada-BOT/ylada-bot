#!/bin/bash

echo "🔄 RESET COMPLETO DO WHATSAPP"
echo "============================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Para todos os processos
echo "1️⃣ Parando servidores..."
pkill -f "whatsapp_server.js" 2>/dev/null
pkill -f "node.*whatsapp" 2>/dev/null
sleep 2
echo -e "${GREEN}✅ Servidores parados${NC}"
echo ""

# 2. Limpa sessões antigas
echo "2️⃣ Limpando sessões antigas..."
rm -rf .wwebjs_auth_* 2>/dev/null
rm -rf .wwebjs_cache_* 2>/dev/null
rm -rf data/sessions/* 2>/dev/null
echo -e "${GREEN}✅ Sessões limpas${NC}"
echo ""

# 3. Aguarda
echo "3️⃣ Aguardando 10 segundos..."
sleep 10
echo -e "${GREEN}✅ Pronto${NC}"
echo ""

# 4. Inicia servidor
echo "4️⃣ Iniciando servidor WhatsApp..."
echo ""
echo "   Execute em outro terminal:"
echo "   ${YELLOW}node whatsapp_server.js${NC}"
echo ""
echo "   Ou pressione Enter para iniciar automaticamente..."
read -p "   (Pressione Enter para continuar ou Ctrl+C para cancelar)"

# Inicia em background
nohup node whatsapp_server.js > whatsapp_server.log 2>&1 &
SERVER_PID=$!

echo ""
echo -e "${GREEN}✅ Servidor iniciado (PID: $SERVER_PID)${NC}"
echo ""

# 5. Aguarda servidor iniciar
echo "5️⃣ Aguardando servidor iniciar (15 segundos)..."
sleep 15

# 6. Testa servidor
echo "6️⃣ Testando servidor..."
if curl -s http://localhost:5001/health > /dev/null; then
    echo -e "${GREEN}✅ Servidor está respondendo!${NC}"
    echo ""
    echo "   Acesse: http://localhost:5002/qr"
    echo "   (ou a URL da sua plataforma)"
else
    echo -e "${RED}❌ Servidor ainda não está respondendo${NC}"
    echo "   Verifique os logs: tail -f whatsapp_server.log"
fi
echo ""

echo "📋 PRÓXIMOS PASSOS:"
echo "==================="
echo "1. Acesse a página de QR Code"
echo "2. Aguarde 30-60 segundos para QR aparecer"
echo "3. Escaneie IMEDIATAMENTE"
echo "4. Se não funcionar, verifique logs: tail -f whatsapp_server.log"
echo ""
