#!/bin/bash

echo "🔗 BOT by YLADA - Iniciando..."
echo ""

# Verifica Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado"
    exit 1
fi

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python não encontrado"
    exit 1
fi

# Instala dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências Node.js..."
    npm install
fi

if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

echo ""
echo "🚀 Iniciando servidor..."
echo "   Acesse: http://localhost:5002"
echo ""

python3 web/app.py


