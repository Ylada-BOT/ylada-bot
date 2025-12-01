#!/bin/bash

# Script para iniciar o servidor WhatsApp Web.js

echo "🚀 Iniciando servidor WhatsApp Web.js..."
echo ""

# Verifica se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não está instalado!"
    echo "Instale em: https://nodejs.org"
    exit 1
fi

# Verifica se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    npm install
fi

# Para processo anterior se existir
if lsof -ti:5001 &> /dev/null; then
    echo "🛑 Parando servidor anterior..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Inicia o servidor
echo "✅ Iniciando servidor na porta 5001..."
echo "📱 O QR Code aparecerá no terminal em alguns segundos"
echo ""
node whatsapp_server.js

