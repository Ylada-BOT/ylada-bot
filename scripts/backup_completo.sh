#!/bin/bash

# ============================================
# Script de Backup Completo - BOT YLADA
# ============================================
# Este script faz backup de TUDO necessário para restaurar o sistema
# ============================================

echo "🔄 Iniciando backup completo do sistema..."

# Criar diretório de backup com data/hora
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Diretório de backup: $BACKUP_DIR"

# ============================================
# 1. BACKUP DO BANCO DE DADOS
# ============================================
echo ""
echo "💾 Fazendo backup do banco de dados..."

# Verifica se DATABASE_URL está configurada
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL não configurada, tentando ler do .env..."
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi
fi

# Extrai informações do DATABASE_URL
if [ ! -z "$DATABASE_URL" ]; then
    # Formato: postgresql://user:password@host:port/database
    DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
    DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    # Backup do PostgreSQL
    if command -v pg_dump &> /dev/null; then
        pg_dump "$DATABASE_URL" > "$BACKUP_DIR/database_backup.sql"
        echo "✅ Backup do banco de dados salvo em: $BACKUP_DIR/database_backup.sql"
    else
        echo "⚠️  pg_dump não encontrado. Instale PostgreSQL client tools."
    fi
else
    echo "⚠️  DATABASE_URL não configurada. Pulando backup do banco."
fi

# ============================================
# 2. BACKUP DAS SESSÕES WHATSAPP
# ============================================
echo ""
echo "📱 Fazendo backup das sessões WhatsApp..."

if [ -d "data/sessions" ]; then
    cp -r data/sessions "$BACKUP_DIR/sessions"
    echo "✅ Sessões WhatsApp salvas em: $BACKUP_DIR/sessions"
else
    echo "⚠️  Diretório data/sessions não encontrado."
fi

# ============================================
# 3. BACKUP DAS CONFIGURAÇÕES
# ============================================
echo ""
echo "⚙️  Fazendo backup das configurações..."

# Arquivo .env
if [ -f .env ]; then
    cp .env "$BACKUP_DIR/.env"
    echo "✅ Arquivo .env salvo"
fi

# Configurações de IA
if [ -f "data/ai_config.json" ]; then
    cp data/ai_config.json "$BACKUP_DIR/ai_config.json"
    echo "✅ Configuração de IA salva"
fi

# Configurações do Flask
if [ -f "web/config.py" ]; then
    cp web/config.py "$BACKUP_DIR/config.py"
    echo "✅ Configuração do Flask salva"
fi

# ============================================
# 4. BACKUP DOS FLUXOS (se salvos em arquivo)
# ============================================
echo ""
echo "🔄 Fazendo backup dos fluxos..."

if [ -f "data/flows.json" ]; then
    cp data/flows.json "$BACKUP_DIR/flows.json"
    echo "✅ Fluxos salvos em arquivo"
fi

# ============================================
# 5. BACKUP DOS LOGS (opcional)
# ============================================
echo ""
echo "📋 Fazendo backup dos logs..."

if [ -d "logs" ]; then
    mkdir -p "$BACKUP_DIR/logs"
    cp -r logs/* "$BACKUP_DIR/logs/" 2>/dev/null || true
    echo "✅ Logs salvos"
fi

# ============================================
# 6. CRIAR ARQUIVO DE INFORMAÇÕES
# ============================================
echo ""
echo "📝 Criando arquivo de informações..."

cat > "$BACKUP_DIR/INFO_BACKUP.txt" << EOF
============================================
BACKUP DO SISTEMA BOT YLADA
============================================
Data/Hora: $(date)
Versão do Sistema: $(git rev-parse HEAD 2>/dev/null || echo "N/A")

CONTEÚDO DO BACKUP:
- database_backup.sql: Backup completo do banco de dados
- sessions/: Sessões WhatsApp (QR codes, autenticações)
- .env: Variáveis de ambiente
- ai_config.json: Configurações de IA
- flows.json: Fluxos salvos em arquivo (se houver)

COMO RESTAURAR:
1. Execute o script: scripts/restore_backup.sh
2. Ou siga as instruções em: GUIA_RESTAURAR_BACKUP.md

IMPORTANTE:
- Mantenha este backup em local seguro
- Não compartilhe o arquivo .env (contém senhas)
- As sessões WhatsApp podem expirar (precisa reconectar)
============================================
EOF

echo "✅ Arquivo de informações criado"

# ============================================
# 7. COMPACTAR TUDO
# ============================================
echo ""
echo "📦 Compactando backup..."

if command -v zip &> /dev/null; then
    zip -r "${BACKUP_DIR}.zip" "$BACKUP_DIR"
    echo "✅ Backup compactado: ${BACKUP_DIR}.zip"
    echo ""
    echo "🗑️  Removendo diretório temporário..."
    rm -rf "$BACKUP_DIR"
    echo "✅ Backup final salvo em: ${BACKUP_DIR}.zip"
elif command -v tar &> /dev/null; then
    tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"
    echo "✅ Backup compactado: ${BACKUP_DIR}.tar.gz"
    echo ""
    echo "🗑️  Removendo diretório temporário..."
    rm -rf "$BACKUP_DIR"
    echo "✅ Backup final salvo em: ${BACKUP_DIR}.tar.gz"
else
    echo "⚠️  zip ou tar não encontrado. Backup não compactado."
    echo "✅ Backup salvo em: $BACKUP_DIR"
fi

# ============================================
# RESUMO
# ============================================
echo ""
echo "============================================"
echo "✅ BACKUP CONCLUÍDO COM SUCESSO!"
echo "============================================"
echo ""
echo "📁 Local do backup:"
if [ -f "${BACKUP_DIR}.zip" ]; then
    echo "   ${BACKUP_DIR}.zip"
elif [ -f "${BACKUP_DIR}.tar.gz" ]; then
    echo "   ${BACKUP_DIR}.tar.gz"
else
    echo "   $BACKUP_DIR"
fi
echo ""
echo "💡 Próximos passos:"
echo "   1. Guarde este backup em local seguro"
echo "   2. Após reiniciar, execute: scripts/restore_backup.sh"
echo "   3. Ou siga: GUIA_RESTAURAR_BACKUP.md"
echo ""
echo "============================================"










