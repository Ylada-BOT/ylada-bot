#!/bin/bash

echo "🚀 Push para GitHub usando Token do .env"
echo ""

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "Execute: ./configurar_env.sh"
    exit 1
fi

# Lê o token do .env
GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$ENV_FILE" 2>/dev/null | cut -d '=' -f2 | tr -d ' ')

if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "cole_seu_token_aqui" ] || [ "$GITHUB_TOKEN" = "" ]; then
    echo "❌ GITHUB_TOKEN não configurado no .env"
    echo ""
    echo "📝 Para configurar:"
    echo "1. Abra o arquivo .env"
    echo "2. Cole seu token na linha GITHUB_TOKEN=..."
    echo "3. Execute este script novamente"
    echo ""
    echo "Ou execute: ./configurar_env.sh"
    exit 1
fi

echo "✅ Token encontrado no .env"
echo ""

# Configura remote com token
echo "🔗 Configurando remote com token..."
git remote set-url origin https://${GITHUB_TOKEN}@github.com/Ylada-BOT/ylada-bot.git

# Faz push
echo "📤 Enviando código para GitHub..."
echo ""

if git push -u origin main 2>&1; then
    echo ""
    echo "✅ ✅ ✅ SUCESSO! Código enviado para GitHub! ✅ ✅ ✅"
    echo ""
    echo "🌐 Acesse: https://github.com/Ylada-BOT/ylada-bot"
    echo ""
    echo "📝 Próximos passos:"
    echo "1. Configure Supabase (veja DEPLOY.md)"
    echo "2. Faça deploy na Vercel"
    echo "3. Adicione variáveis de ambiente no Vercel"
else
    echo ""
    echo "❌ Erro ao fazer push"
    echo "Verifique se:"
    echo "1. O token está correto no .env"
    echo "2. O repositório existe no GitHub"
    echo "3. Você tem permissão no repositório"
    exit 1
fi

