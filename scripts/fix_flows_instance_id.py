#!/usr/bin/env python3
"""
Script para adicionar a coluna instance_id na tabela flows
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.database import engine
from sqlalchemy import text

def fix_flows_table():
    """Adiciona a coluna instance_id na tabela flows"""
    print("🔧 Adicionando coluna instance_id na tabela flows...")
    
    sql = """
    -- Adiciona a coluna instance_id
    ALTER TABLE flows 
    ADD COLUMN IF NOT EXISTS instance_id INTEGER REFERENCES instances(id);
    
    -- Cria índice para melhor performance
    CREATE INDEX IF NOT EXISTS idx_flows_instance_id ON flows(instance_id);
    
    -- Comentário para documentação
    COMMENT ON COLUMN flows.instance_id IS 'ID da instância (NULL = fluxo compartilhado entre todas as instâncias)';
    """
    
    try:
        with engine.connect() as conn:
            # Executa cada comando separadamente
            commands = [
                "ALTER TABLE flows ADD COLUMN IF NOT EXISTS instance_id INTEGER REFERENCES instances(id);",
                "CREATE INDEX IF NOT EXISTS idx_flows_instance_id ON flows(instance_id);"
            ]
            
            for cmd in commands:
                try:
                    conn.execute(text(cmd))
                    conn.commit()
                    print(f"✅ Executado: {cmd[:50]}...")
                except Exception as e:
                    # Ignora erro se coluna/índice já existir
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"⚠️  Já existe: {cmd[:50]}...")
                    else:
                        print(f"❌ Erro: {e}")
                        raise
            
            print("\n✅ Coluna instance_id adicionada com sucesso!")
            return True
            
    except Exception as e:
        print(f"\n❌ Erro ao executar SQL: {e}")
        return False

if __name__ == '__main__':
    success = fix_flows_table()
    sys.exit(0 if success else 1)
