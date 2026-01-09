#!/usr/bin/env python3
"""
Script para testar conexão com banco de dados Supabase
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

def test_connection():
    """Testa conexão com banco de dados"""
    print("=" * 60)
    print("🔍 Testando Conexão com Supabase")
    print("=" * 60)
    print()
    
    # Verifica se .env.local existe
    env_file = root_dir / '.env.local'
    if not env_file.exists():
        print("❌ Arquivo .env.local não encontrado!")
        print(f"   Crie o arquivo em: {env_file}")
        print()
        print("   Exemplo de conteúdo:")
        print("   DATABASE_URL=postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres")
        return False
    
    print(f"✅ Arquivo .env.local encontrado: {env_file}")
    
    # Carrega variáveis de ambiente
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("✅ Variáveis de ambiente carregadas")
    except ImportError:
        print("❌ python-dotenv não instalado")
        print("   Instale com: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Erro ao carregar .env.local: {e}")
        return False
    
    # Verifica se DATABASE_URL está configurada
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não configurada no .env.local")
        print("   Adicione a linha: DATABASE_URL=...")
        return False
    
    print("✅ DATABASE_URL encontrada")
    
    # Mostra connection string (mascarada)
    masked_url = mask_database_url(database_url)
    print(f"   Connection string: {masked_url}")
    print()
    
    # Tenta conectar
    print("🔄 Tentando conectar ao banco de dados...")
    try:
        from config.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            # Testa query simples
            result = conn.execute(text('SELECT 1 as test'))
            row = result.fetchone()
            
            if row and row[0] == 1:
                print("✅ Conexão bem-sucedida!")
                print()
                
                # Tenta verificar tabelas
                print("🔄 Verificando tabelas...")
                try:
                    result = conn.execute(text("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        ORDER BY table_name
                    """))
                    tables = [row[0] for row in result]
                    
                    if tables:
                        print(f"✅ {len(tables)} tabela(s) encontrada(s):")
                        for table in tables[:10]:  # Mostra até 10
                            print(f"   - {table}")
                        if len(tables) > 10:
                            print(f"   ... e mais {len(tables) - 10} tabela(s)")
                    else:
                        print("⚠️  Nenhuma tabela encontrada no schema 'public'")
                        print("   Execute o script SQL para criar as tabelas")
                except Exception as e:
                    print(f"⚠️  Não foi possível listar tabelas: {e}")
                
                return True
            else:
                print("❌ Conexão retornou resultado inesperado")
                return False
                
    except Exception as e:
        error_msg = str(e)
        print("❌ Erro ao conectar:")
        print(f"   {error_msg}")
        print()
        
        # Dá dicas baseadas no erro
        if 'Tenant or user not found' in error_msg or 'FATAL' in error_msg:
            print("💡 DICAS:")
            print("   1. Verifique se o projeto Supabase está ativo (não pausado)")
            print("   2. Verifique se a senha do banco está correta")
            print("   3. Se a senha tem caracteres especiais, codifique-os:")
            print("      @ → %40, # → %23, % → %25, etc.")
            print("   4. Verifique se a connection string está no formato correto")
            print("   5. Tente resetar a senha do banco no Supabase")
        elif 'could not translate host name' in error_msg.lower():
            print("💡 DICA: Verifique se o hostname está correto na connection string")
        elif 'password authentication failed' in error_msg.lower():
            print("💡 DICA: A senha do banco está incorreta. Verifique ou resete no Supabase")
        elif 'timeout' in error_msg.lower():
            print("💡 DICA: Timeout na conexão. Verifique sua internet ou firewall")
        
        return False

def mask_database_url(url):
    """Mascara a senha na connection string para exibição"""
    try:
        # Formato: postgresql://user:password@host:port/db
        if '@' in url:
            parts = url.split('@')
            if len(parts) == 2:
                auth_part = parts[0]
                rest = parts[1]
                
                if '://' in auth_part:
                    protocol_user = auth_part.split('://')
                    if len(protocol_user) == 2:
                        protocol = protocol_user[0]
                        user_pass = protocol_user[1]
                        
                        if ':' in user_pass:
                            user = user_pass.split(':')[0]
                            return f"{protocol}://{user}:***@{rest}"
        
        # Se não conseguir parsear, retorna mascarado
        if '://' in url and '@' in url:
            return url.split('://')[0] + '://***@' + url.split('@')[1]
        
        return "***"
    except:
        return "***"

if __name__ == '__main__':
    success = test_connection()
    print()
    print("=" * 60)
    if success:
        print("✅ Teste concluído com sucesso!")
        sys.exit(0)
    else:
        print("❌ Teste falhou. Verifique as dicas acima.")
        sys.exit(1)

