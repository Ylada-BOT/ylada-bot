#!/usr/bin/env python3
"""
Script para atualizar a senha do usuário portalmagra no banco de dados
Gera hash bcrypt correto e atualiza no banco
"""
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.auth.authentication import hash_password
    from src.database.db import SessionLocal
    from src.models.user import User
    
    # Gera hash bcrypt da senha "123456"
    password = "123456"
    password_hash = hash_password(password)
    
    print(f"Hash bcrypt gerado: {password_hash}")
    print(f"\nAtualizando senha do usuário portalmagra@gmail.com...")
    
    # Conecta ao banco
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == 'portalmagra@gmail.com').first()
        
        if not user:
            print(f"❌ Usuário portalmagra@gmail.com não encontrado no banco!")
            sys.exit(1)
        
        # Atualiza a senha
        user.password_hash = password_hash
        db.commit()
        
        print(f"✅ Senha atualizada com sucesso!")
        print(f"   Email: {user.email}")
        print(f"   Nome: {user.name}")
        print(f"   ID: {user.id}")
        
        # Verifica se a senha funciona
        from src.auth.authentication import verify_password
        if verify_password("123456", user.password_hash):
            print(f"✅ Verificação: Senha está correta!")
        else:
            print(f"❌ Verificação: Senha NÃO está correta!")
            
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print(f"   Execute: pip install bcrypt sqlalchemy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

