#!/bin/bash

echo "🔍 DIAGNÓSTICO COMPLETO DO WHATSAPP"
echo "===================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verifica se servidor Node.js está rodando
echo "1️⃣ Verificando servidor Node.js..."
if pgrep -f "whatsapp_server.js" > /dev/null; then
    echo -e "${GREEN}✅ Servidor WhatsApp está rodando${NC}"
    SERVER_PID=$(pgrep -f "whatsapp_server.js" | head -1)
    echo "   PID: $SERVER_PID"
else
    echo -e "${RED}❌ Servidor WhatsApp NÃO está rodando${NC}"
    echo "   Execute: node whatsapp_server.js"
fi
echo ""

# 2. Verifica se porta está aberta
echo "2️⃣ Verificando porta 5001..."
if lsof -i :5001 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Porta 5001 está aberta${NC}"
    lsof -i :5001
else
    echo -e "${RED}❌ Porta 5001 NÃO está aberta${NC}"
fi
echo ""

# 3. Testa se servidor responde
echo "3️⃣ Testando resposta do servidor..."
if curl -s http://localhost:5001/health > /dev/null; then
    echo -e "${GREEN}✅ Servidor responde em /health${NC}"
    curl -s http://localhost:5001/health | jq . 2>/dev/null || curl -s http://localhost:5001/health
else
    echo -e "${RED}❌ Servidor NÃO responde em /health${NC}"
fi
echo ""

# 4. Verifica sessões antigas
echo "4️⃣ Verificando sessões antigas..."
SESSION_COUNT=$(find . -maxdepth 1 -name ".wwebjs_auth_*" -o -name ".wwebjs_cache_*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SESSION_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}⚠️ Encontradas $SESSION_COUNT sessões antigas${NC}"
    echo "   Sessões encontradas:"
    find . -maxdepth 1 -name ".wwebjs_auth_*" -o -name ".wwebjs_cache_*" 2>/dev/null | head -5
    echo ""
    echo "   💡 Recomendação: Limpar sessões antigas"
    echo "   Execute: rm -rf .wwebjs_auth_* .wwebjs_cache_*"
else
    echo -e "${GREEN}✅ Nenhuma sessão antiga encontrada${NC}"
fi
echo ""

# 5. Verifica dependências Node.js
echo "5️⃣ Verificando dependências Node.js..."
if [ -f "package.json" ]; then
    if [ -d "node_modules" ]; then
        echo -e "${GREEN}✅ node_modules existe${NC}"
        
        # Verifica se whatsapp-web.js está instalado
        if [ -d "node_modules/whatsapp-web.js" ]; then
            echo -e "${GREEN}✅ whatsapp-web.js está instalado${NC}"
        else
            echo -e "${RED}❌ whatsapp-web.js NÃO está instalado${NC}"
            echo "   Execute: npm install"
        fi
    else
        echo -e "${RED}❌ node_modules NÃO existe${NC}"
        echo "   Execute: npm install"
    fi
else
    echo -e "${RED}❌ package.json não encontrado${NC}"
fi
echo ""

# 6. Verifica Flask
echo "6️⃣ Verificando servidor Flask..."
if pgrep -f "app.py\|flask\|gunicorn" > /dev/null; then
    echo -e "${GREEN}✅ Servidor Flask está rodando${NC}"
else
    echo -e "${YELLOW}⚠️ Servidor Flask NÃO está rodando${NC}"
    echo "   (Pode estar rodando em outro processo)"
fi
echo ""

# 7. Verifica logs recentes
echo "7️⃣ Últimas linhas do log (se existir)..."
if [ -f "whatsapp_server.log" ]; then
    echo "   Últimas 10 linhas:"
    tail -10 whatsapp_server.log 2>/dev/null || echo "   (Não foi possível ler o log)"
else
    echo "   (Nenhum arquivo de log encontrado)"
fi
echo ""

# 8. Verifica memória e recursos
echo "8️⃣ Verificando recursos do sistema..."
echo "   Memória disponível:"
free -h 2>/dev/null || vm_stat | head -5
echo ""

# 9. Testa endpoint /qr
echo "9️⃣ Testando endpoint /qr..."
QR_RESPONSE=$(curl -s "http://localhost:5001/qr?user_id=test" 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Endpoint /qr responde${NC}"
    echo "$QR_RESPONSE" | head -3
else
    echo -e "${RED}❌ Endpoint /qr NÃO responde${NC}"
    echo "   Erro: $QR_RESPONSE"
fi
echo ""

# 10. Recomendações
echo "📋 RECOMENDAÇÕES:"
echo "=================="
echo ""
echo "Se o servidor NÃO está rodando:"
echo "  1. node whatsapp_server.js"
echo ""
echo "Se há sessões antigas:"
echo "  1. pkill -f whatsapp_server.js"
echo "  2. rm -rf .wwebjs_auth_* .wwebjs_cache_*"
echo "  3. node whatsapp_server.js"
echo ""
echo "Se o QR Code não aparece:"
echo "  1. Aguarde 30-60 segundos após iniciar servidor"
echo "  2. Recarregue a página (F5)"
echo "  3. Verifique logs do servidor"
echo ""
echo "Se nada funcionar:"
echo "  1. Considere usar API oficial da Meta"
echo "  2. Ou use BSP (Twilio, 360dialog)"
echo ""
