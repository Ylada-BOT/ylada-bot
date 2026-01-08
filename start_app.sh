#!/bin/bash
# Script wrapper que detecta automaticamente o comando Python disponível

# Detecta qual comando Python está disponível
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Erro: Python não encontrado. Instale Python 3.6 ou superior."
    exit 1
fi

# Verifica versão do Python
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Usando: $PYTHON_CMD (versão $PYTHON_VERSION)"

# Executa a aplicação
exec $PYTHON_CMD web/app.py

