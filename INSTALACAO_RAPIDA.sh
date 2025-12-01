#!/bin/bash

echo "🚀 Instalação Rápida - Bot Ylada"
echo "=================================="
echo ""

# Verifica Python
echo "📦 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python não encontrado!"
    echo "   Baixe em: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION encontrado"
echo ""

# Cria ambiente virtual
echo "🔧 Criando ambiente virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi
echo ""

# Ativa ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source .venv/bin/activate
echo "✅ Ambiente ativado"
echo ""

# Instala dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# Verifica configuração
echo "⚙️  Verificando configuração..."
if [ ! -f "config/config.yaml" ]; then
    echo "⚠️  config/config.yaml não encontrado"
    if [ -f "config/config.example.yaml" ]; then
        cp config/config.example.yaml config/config.yaml
        echo "✅ Criado config/config.yaml a partir do exemplo"
        echo "⚠️  IMPORTANTE: Edite config/config.yaml se necessário"
    fi
else
    echo "✅ Configuração encontrada"
fi
echo ""

echo "✅ Instalação completa!"
echo ""
echo "🚀 Para iniciar o bot:"
echo "   source .venv/bin/activate"
echo "   python web/app.py"
echo ""
echo "📖 Acesse: http://localhost:5001"
echo ""

