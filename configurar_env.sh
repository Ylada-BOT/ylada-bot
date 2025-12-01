#!/bin/bash

echo "🔐 Configurador de .env - Ylada BOT"
echo ""

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi

echo "📝 Preencha as informações abaixo:"
echo ""

# Supabase
read -p "Supabase URL: " SUPABASE_URL
read -p "Supabase Key (anon): " SUPABASE_KEY
read -p "Supabase Service Key: " SUPABASE_SERVICE_KEY

# GitHub Token
read -p "GitHub Token: " GITHUB_TOKEN

# Secret Key
read -p "Secret Key (ou pressione Enter para gerar): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo "✅ Secret Key gerada automaticamente"
fi

# Atualiza o arquivo .env
cat > "$ENV_FILE" << EOF
# Configurações Locais - NÃO COMMITAR
BOT_MODE=webjs
PORT=5002

# Supabase Database
SUPABASE_URL=$SUPABASE_URL
SUPABASE_KEY=$SUPABASE_KEY
SUPABASE_SERVICE_KEY=$SUPABASE_SERVICE_KEY

# GitHub Token
GITHUB_TOKEN=$GITHUB_TOKEN

# Z-API (Opcional)
ZAPI_INSTANCE_ID=
ZAPI_TOKEN=

# WhatsApp Web.js
WHATSAPP_SERVER_PORT=5001

# Segurança
SECRET_KEY=$SECRET_KEY

# Ambiente
ENVIRONMENT=local
EOF

echo ""
echo "✅ Arquivo .env configurado com sucesso!"
echo "⚠️  Lembre-se: Este arquivo NÃO será commitado (está no .gitignore)"

