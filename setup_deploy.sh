#!/bin/bash

echo "🚀 Configurando Ylada BOT para Deploy"
echo ""

# Verifica se está no diretório correto
if [ ! -f "web/app.py" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto"
    exit 1
fi

# 1. Verifica Git
if [ ! -d ".git" ]; then
    echo "📦 Inicializando Git..."
    git init
    echo "✅ Git inicializado"
else
    echo "✅ Git já inicializado"
fi

# 2. Verifica .gitignore
if [ ! -f ".gitignore" ]; then
    echo "📝 Criando .gitignore..."
    # Já foi criado
    echo "✅ .gitignore criado"
else
    echo "✅ .gitignore existe"
fi

# 3. Verifica requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: requirements.txt não encontrado"
    exit 1
else
    echo "✅ requirements.txt encontrado"
fi

# 4. Verifica vercel.json
if [ ! -f "vercel.json" ]; then
    echo "❌ Erro: vercel.json não encontrado"
    exit 1
else
    echo "✅ vercel.json encontrado"
fi

echo ""
echo "✅ Projeto pronto para deploy!"
echo ""
echo "📋 Próximos passos:"
echo "1. git add ."
echo "2. git commit -m 'Ready for deploy'"
echo "3. git remote add origin https://github.com/SEU-USUARIO/ylada-bot.git"
echo "4. git push -u origin main"
echo "5. Acesse https://vercel.com e importe o repositório"
echo ""
echo "📖 Veja DEPLOY.md para instruções completas"

