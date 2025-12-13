#!/usr/bin/env python3
"""
Script para inicializar banco de dados
Cria tabelas e dados iniciais
"""
import sys
import os

# Adiciona diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db import init_db, SessionLocal
from src.models import User, Tenant, Plan, Subscription
from src.models.user import UserRole
from src.models.subscription import SubscriptionStatus
from src.auth.authentication import hash_password
from config.settings import DEFAULT_PLANS


def create_default_plans(db):
    """Cria planos padrão"""
    print("[*] Criando planos padrão...")
    
    for plan_key, plan_data in DEFAULT_PLANS.items():
        existing = db.query(Plan).filter(Plan.name == plan_data['name']).first()
        if existing:
            print(f"  [✓] Plano '{plan_data['name']}' já existe")
            continue
        
        plan = Plan(
            name=plan_data['name'],
            description=f"Plano {plan_data['name']}",
            price=plan_data['price'],
            max_instances=plan_data['max_instances'],
            max_flows=plan_data['max_flows'],
            max_messages_month=plan_data['max_messages_month'],
            features=plan_data['features'],
            is_active=True
        )
        
        db.add(plan)
        print(f"  [✓] Plano '{plan_data['name']}' criado")
    
    db.commit()
    print("[✓] Planos criados com sucesso!")


def create_admin_user(db):
    """Cria usuário admin padrão"""
    print("[*] Criando usuário admin...")
    
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@ylada.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        print(f"  [✓] Usuário admin já existe: {admin_email}")
        return existing
    
    admin = User(
        email=admin_email,
        password_hash=hash_password(admin_password),
        name='Administrador',
        role=UserRole.ADMIN,
        is_active=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"  [✓] Usuário admin criado: {admin_email} / {admin_password}")
    print(f"  [!] IMPORTANTE: Altere a senha após o primeiro login!")
    
    return admin


def main():
    """Função principal"""
    print("\n" + "="*50)
    print("🚀 Inicializando banco de dados")
    print("="*50 + "\n")
    
    # Verifica se DATABASE_URL está configurado
    database_url = os.getenv('DATABASE_URL')
    if not database_url or 'password@localhost' in database_url:
        print("[!] ATENÇÃO: DATABASE_URL não configurado!")
        print("[!] Configure a variável de ambiente DATABASE_URL")
        print("[!] Exemplo: export DATABASE_URL='postgresql://user:pass@host:5432/db'")
        print("[!] Ou crie arquivo .env com: DATABASE_URL=...")
        print()
        print("[*] Para Supabase:")
        print("    1. Acesse: https://supabase.com")
        print("    2. Crie um projeto")
        print("    3. Vá em Settings > Database > Connection string")
        print("    4. Copie a URI e configure no .env")
        print()
        resposta = input("Deseja continuar mesmo assim? (s/N): ")
        if resposta.lower() != 's':
            print("[*] Cancelado. Configure DATABASE_URL e tente novamente.")
            sys.exit(1)
    
    try:
        # Inicializa banco (cria tabelas)
        print("[*] Criando tabelas...")
        init_db()
        print("[✓] Tabelas criadas com sucesso!\n")
        
        # Cria dados iniciais
        db = SessionLocal()
        try:
            create_default_plans(db)
            print()
            create_admin_user(db)
            print()
            
            print("="*50)
            print("✅ Banco de dados inicializado com sucesso!")
            print("="*50 + "\n")
            print("📝 Próximos passos:")
            print("   1. Acesse: http://localhost:5002/register")
            print("   2. Crie sua conta")
            print("   3. Ou use o usuário admin criado")
            print()
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n[!] Erro ao inicializar banco de dados: {e}")
        print("\n[!] Dicas:")
        print("   - Verifique se DATABASE_URL está correto")
        print("   - Verifique se o banco de dados está acessível")
        print("   - Para Supabase: verifique se o projeto está ativo")
        print("   - Execute o script SQL manualmente se necessário:")
        print("     scripts/create_tables_supabase.sql")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
