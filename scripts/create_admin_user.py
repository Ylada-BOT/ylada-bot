#!/usr/bin/env python3
"""
Script para criar usuário administrador no banco de dados Supabase
"""
import sys
import os
import bcrypt

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def hash_password(password: str) -> str:
    """Gera hash bcrypt da senha"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def main():
    """Cria usuário administrador"""
    email = "faulaandre@gmail.com"
    password = "Hbl@0842"
    name = "Deise"
    
    # Gera hash da senha
    password_hash = hash_password(password)
    
    print("=" * 60)
    print("CRIAR USUÁRIO ADMINISTRADOR")
    print("=" * 60)
    print(f"Email: {email}")
    print(f"Nome: {name}")
    print(f"Role: admin")
    print()
    print("Hash da senha gerado:")
    print(password_hash)
    print()
    print("=" * 60)
    print("SQL PARA EXECUTAR NO SUPABASE:")
    print("=" * 60)
    print()
    
    sql = f"""-- Criar usuário administrador
INSERT INTO users (email, password_hash, name, role, is_active)
VALUES (
    '{email}',
    '{password_hash}',
    '{name}',
    'admin',
    true
)
ON CONFLICT (email) 
DO UPDATE SET
    password_hash = EXCLUDED.password_hash,
    name = EXCLUDED.name,
    role = EXCLUDED.role,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- Verificar se usuário foi criado
SELECT id, email, name, role, is_active, created_at 
FROM users 
WHERE email = '{email}';
"""
    
    print(sql)
    print()
    print("=" * 60)
    print("INSTRUÇÕES:")
    print("=" * 60)
    print("1. Copie o SQL acima")
    print("2. Acesse: https://supabase.com")
    print("3. Vá em SQL Editor > New query")
    print("4. Cole o SQL e execute (Run)")
    print("5. Verifique se o usuário foi criado")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("ERRO: Módulo bcrypt não encontrado")
        print()
        print("Instale o bcrypt:")
        print("  pip install bcrypt")
        print()
        print("Ou use o venv do projeto:")
        print("  source venv/bin/activate")
        print("  pip install bcrypt")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

