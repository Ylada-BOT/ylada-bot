#!/bin/bash

# Script para limpar sessões do WhatsApp que podem estar causando problemas de conexão

echo "🧹 Limpando sessões do WhatsApp..."
echo ""

# Para todos os processos do WhatsApp
echo "⏹️  Parando processos do WhatsApp..."
pkill -f "whatsapp_server.js" || true
pkill -f "node.*whatsapp" || true
sleep 2

# Limpa sessões antigas
echo "🗑️  Removendo sessões antigas..."
rm -rf .wwebjs_auth_* 2>/dev/null || true
rm -rf .wwebjs_cache_* 2>/dev/null || true
rm -rf data/sessions/* 2>/dev/null || true

echo ""
echo "✅ Limpeza concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Reinicie o servidor WhatsApp"
echo "2. Acesse a página de conexão"
echo "3. Escaneie o QR Code novamente"
echo ""
echo "⚠️  IMPORTANTE: Cada telefone precisa ter sua própria instância!"
echo "   Se você está tentando conectar 2 telefones, crie 2 instâncias diferentes."

