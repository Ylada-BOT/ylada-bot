#!/bin/bash
# Script para criar versão transparente do logo
# Remove fundo branco e cria PNG com transparência

cd "$(dirname "$0")/.."

LOGO_INPUT="web/static/assets/logo.png"
LOGO_OUTPUT="web/static/assets/logo_transparent.png"

echo "🎨 Criando versão transparente do logo..."

# Verifica se imagemagick está instalado
if command -v convert &> /dev/null; then
    # Remove fundo branco e cria versão transparente
    convert "$LOGO_INPUT" -fuzz 10% -transparent white "$LOGO_OUTPUT"
    echo "✅ Logo transparente criado: $LOGO_OUTPUT"
elif command -v sips &> /dev/null; then
    # macOS - usa sips para criar cópia (não remove fundo, mas mantém formato)
    cp "$LOGO_INPUT" "$LOGO_OUTPUT"
    echo "✅ Cópia criada (use imagemagick para remover fundo): $LOGO_OUTPUT"
    echo "💡 Instale imagemagick: brew install imagemagick"
else
    echo "⚠️ Instale imagemagick para criar logo transparente:"
    echo "   macOS: brew install imagemagick"
    echo "   Linux: sudo apt-get install imagemagick"
fi

