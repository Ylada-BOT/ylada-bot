#!/bin/bash

echo "🚀 Script de Push para GitHub - Ylada BOT"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se está no diretório correto
if [ ! -f "web/app.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script na raiz do projeto${NC}"
    exit 1
fi

# Verifica se já tem commit
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Nenhum commit encontrado. Fazendo commit inicial...${NC}"
    git add .
    git commit -m "Ylada BOT - Initial commit with full features"
fi

# Pergunta qual é o nome do usuário/organização
echo -e "${YELLOW}Qual é o nome do seu usuário/organização no GitHub?${NC}"
echo "1. YladaLead (usuário pessoal)"
echo "2. Ylada-BOT (organização)"
echo "3. Outro (digite o nome)"
read -p "Escolha (1/2/3): " choice

case $choice in
    1)
        GITHUB_USER="YladaLead"
        ;;
    2)
        GITHUB_USER="Ylada-BOT"
        ;;
    3)
        read -p "Digite o nome do usuário/organização: " GITHUB_USER
        ;;
    *)
        echo -e "${RED}Opção inválida. Usando YladaLead como padrão.${NC}"
        GITHUB_USER="YladaLead"
        ;;
esac

REPO_URL="https://github.com/${GITHUB_USER}/ylada-bot.git"

echo ""
echo -e "${YELLOW}📋 Verificando configuração...${NC}"

# Remove remote existente se houver
git remote remove origin 2>/dev/null

# Adiciona novo remote
echo -e "${YELLOW}🔗 Conectando ao repositório: ${REPO_URL}${NC}"
git remote add origin "$REPO_URL"

# Verifica branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}🔄 Renomeando branch para 'main'...${NC}"
    git branch -M main
fi

# Tenta fazer push
echo ""
echo -e "${YELLOW}📤 Enviando código para GitHub...${NC}"
echo ""

if git push -u origin main 2>&1; then
    echo ""
    echo -e "${GREEN}✅ Sucesso! Código enviado para GitHub!${NC}"
    echo ""
    echo -e "${GREEN}🌐 Acesse: https://github.com/${GITHUB_USER}/ylada-bot${NC}"
    echo ""
    echo -e "${YELLOW}📝 Próximos passos:${NC}"
    echo "1. Configure Supabase (veja DEPLOY.md)"
    echo "2. Faça deploy na Vercel"
    echo "3. Adicione variáveis de ambiente"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Erro ao fazer push!${NC}"
    echo ""
    echo -e "${YELLOW}Possíveis causas:${NC}"
    echo "1. Repositório não existe no GitHub"
    echo "2. Você não tem permissão"
    echo "3. Problema de autenticação"
    echo ""
    echo -e "${YELLOW}🔧 Solução:${NC}"
    echo "1. Acesse: https://github.com/new"
    echo "2. Crie um repositório chamado: ${GREEN}ylada-bot${NC}"
    echo "3. ${RED}NÃO${NC} marque 'Add README', 'Add .gitignore' ou 'Add license'"
    echo "4. Clique em 'Create repository'"
    echo "5. Execute este script novamente: ${GREEN}./push_to_github.sh${NC}"
    echo ""
    exit 1
fi

