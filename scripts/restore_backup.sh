#!/bin/bash

# ============================================
# Script de Restauração - BOT YLADA
# ============================================
# Este script restaura um backup completo do sistema
# ============================================

echo "🔄 Iniciando restauração do backup..."

# Verifica se foi passado o arquivo de backup
if [ -z "$1" ]; then
    echo "❌ Erro: Especifique o arquivo de backup"
    echo ""
    echo "Uso: ./restore_backup.sh <arquivo_backup>"
    echo ""
    echo "Exemplos:"
    echo "  ./restore_backup.sh backup_20241223_120000.zip"
    echo "  ./restore_backup.sh backup_20241223_120000.tar.gz"
    echo "  ./restore_backup.sh backup_20241223_120000"
    exit 1
fi

BACKUP_FILE="$1"

# Verifica se o arquivo existe
if [ ! -f "$BACKUP_FILE" ] && [ ! -d "$BACKUP_FILE" ]; then
    echo "❌ Erro: Arquivo de backup não encontrado: $BACKUP_FILE"
    exit 1
fi

# Criar diretório temporário para extração
TEMP_DIR="restore_temp_$(date +%s)"
mkdir -p "$TEMP_DIR"

echo "📦 Extraindo backup..."

# Extrai o backup
if [[ "$BACKUP_FILE" == *.zip ]]; then
    unzip -q "$BACKUP_FILE" -d "$TEMP_DIR"
    BACKUP_DIR=$(ls -d "$TEMP_DIR"/*/ | head -1)
elif [[ "$BACKUP_FILE" == *.tar.gz ]] || [[ "$BACKUP_FILE" == *.tgz ]]; then
    tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
    BACKUP_DIR=$(ls -d "$TEMP_DIR"/*/ | head -1)
else
    # Assume que é um diretório
    BACKUP_DIR="$BACKUP_FILE"
fi

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Erro: Não foi possível extrair o backup"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "✅ Backup extraído em: $BACKUP_DIR"

# ============================================
# 1. RESTAURAR BANCO DE DADOS
# ============================================
echo ""
echo "💾 Restaurando banco de dados..."

if [ -f "$BACKUP_DIR/database_backup.sql" ]; then
    # Verifica se DATABASE_URL está configurada
    if [ -z "$DATABASE_URL" ]; then
        if [ -f .env ]; then
            export $(grep -v '^#' .env | xargs)
        fi
    fi
    
    if [ ! -z "$DATABASE_URL" ]; then
        if command -v psql &> /dev/null; then
            echo "⚠️  ATENÇÃO: Isso vai SOBRESCREVER o banco de dados atual!"
            read -p "   Deseja continuar? (s/N): " confirm
            if [[ $confirm == [sS] ]]; then
                psql "$DATABASE_URL" < "$BACKUP_DIR/database_backup.sql"
                echo "✅ Banco de dados restaurado"
            else
                echo "⏭️  Restauração do banco cancelada"
            fi
        else
            echo "⚠️  psql não encontrado. Instale PostgreSQL client tools."
        fi
    else
        echo "⚠️  DATABASE_URL não configurada. Pulando restauração do banco."
    fi
else
    echo "⚠️  Arquivo database_backup.sql não encontrado no backup"
fi

# ============================================
# 2. RESTAURAR SESSÕES WHATSAPP
# ============================================
echo ""
echo "📱 Restaurando sessões WhatsApp..."

if [ -d "$BACKUP_DIR/sessions" ]; then
    mkdir -p data/sessions
    cp -r "$BACKUP_DIR/sessions"/* data/sessions/
    echo "✅ Sessões WhatsApp restauradas"
    echo "⚠️  NOTA: Você pode precisar reconectar alguns WhatsApps"
else
    echo "⚠️  Diretório sessions não encontrado no backup"
fi

# ============================================
# 3. RESTAURAR CONFIGURAÇÕES
# ============================================
echo ""
echo "⚙️  Restaurando configurações..."

# Arquivo .env
if [ -f "$BACKUP_DIR/.env" ]; then
    echo "⚠️  ATENÇÃO: Isso vai SOBRESCREVER seu arquivo .env atual!"
    read -p "   Deseja continuar? (s/N): " confirm
    if [[ $confirm == [sS] ]]; then
        cp "$BACKUP_DIR/.env" .env
        echo "✅ Arquivo .env restaurado"
    else
        echo "⏭️  Restauração do .env cancelada"
    fi
fi

# Configurações de IA
if [ -f "$BACKUP_DIR/ai_config.json" ]; then
    mkdir -p data
    cp "$BACKUP_DIR/ai_config.json" data/ai_config.json
    echo "✅ Configuração de IA restaurada"
fi

# Configurações do Flask
if [ -f "$BACKUP_DIR/config.py" ]; then
    cp "$BACKUP_DIR/config.py" web/config.py
    echo "✅ Configuração do Flask restaurada"
fi

# ============================================
# 4. RESTAURAR FLUXOS
# ============================================
echo ""
echo "🔄 Restaurando fluxos..."

if [ -f "$BACKUP_DIR/flows.json" ]; then
    mkdir -p data
    cp "$BACKUP_DIR/flows.json" data/flows.json
    echo "✅ Fluxos restaurados"
fi

# ============================================
# 5. RESTAURAR LOGS (opcional)
# ============================================
echo ""
echo "📋 Restaurando logs..."

if [ -d "$BACKUP_DIR/logs" ]; then
    mkdir -p logs
    cp -r "$BACKUP_DIR/logs"/* logs/ 2>/dev/null || true
    echo "✅ Logs restaurados"
fi

# ============================================
# LIMPEZA
# ============================================
echo ""
echo "🧹 Limpando arquivos temporários..."
rm -rf "$TEMP_DIR"

# ============================================
# RESUMO
# ============================================
echo ""
echo "============================================"
echo "✅ RESTAURAÇÃO CONCLUÍDA!"
echo "============================================"
echo ""
echo "💡 Próximos passos:"
echo "   1. Verifique se o banco de dados foi restaurado"
echo "   2. Verifique as sessões WhatsApp (pode precisar reconectar)"
echo "   3. Reinicie o servidor: python web/app.py"
echo "   4. Verifique se tudo está funcionando"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Sessões WhatsApp podem ter expirado"
echo "   - Você pode precisar escanear QR codes novamente"
echo ""
echo "============================================"










