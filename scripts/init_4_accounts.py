"""
Script para inicializar 4 contas e instâncias WhatsApp
Execute este script uma vez para configurar seus 4 telefones
"""
import sys
import os
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database import Database
from instance_manager import InstanceManager
from account_manager import AccountManager


def init_accounts():
    """Inicializa 4 contas e instâncias"""
    
    print("=" * 60)
    print("🚀 Inicializando 4 Contas WhatsApp")
    print("=" * 60)
    
    # Conecta ao banco
    db = Database(use_sqlite=True)  # Usa SQLite por padrão (pode mudar depois)
    account_manager = AccountManager(db)
    instance_manager = InstanceManager(db)
    
    # Verifica se já existem contas
    existing_accounts = account_manager.get_all_accounts()
    if existing_accounts:
        print(f"\n[!] Já existem {len(existing_accounts)} contas no banco.")
        resposta = input("Deseja criar novas contas? (s/n): ")
        if resposta.lower() != 's':
            print("[*] Cancelado.")
            return
    
    # Solicita os 4 números
    print("\n📱 Informe seus 4 números WhatsApp:")
    print("   Formato: 5511999999999 (código do país + DDD + número)")
    print()
    
    accounts_data = []
    ports = [5001, 5002, 5003, 5004]
    
    for i in range(4):
        while True:
            phone = input(f"Telefone {i+1}: ").strip()
            if phone:
                name = input(f"  Nome da conta {i+1} (opcional): ").strip() or f"Conta {i+1}"
                accounts_data.append({
                    'name': name,
                    'phone': phone,
                    'port': ports[i]
                })
                break
            else:
                print("  [!] Número é obrigatório!")
    
    # Cria contas e instâncias
    print("\n[*] Criando contas e instâncias...")
    
    for i, acc_data in enumerate(accounts_data):
        # Cria conta
        account = account_manager.create_account(
            name=acc_data['name'],
            phone=acc_data['phone'],
            plan='owner'
        )
        print(f"[✓] Conta criada: {account['name']} ({account['phone']})")
        
        # Cria instância
        instance = instance_manager.create_instance_for_account(
            account_id=account['id'],
            instance_name=f"instance_{acc_data['phone']}",
            port=acc_data['port']
        )
        print(f"[✓] Instância criada: porta {instance['port']}")
    
    print("\n" + "=" * 60)
    print("✅ Configuração concluída!")
    print("=" * 60)
    print("\n📋 Próximos passos:")
    print("1. Inicie o servidor: python web/app.py")
    print("2. Acesse: http://localhost:5002")
    print("3. Conecte cada telefone escaneando o QR Code")
    print()


if __name__ == '__main__':
    try:
        init_accounts()
    except KeyboardInterrupt:
        print("\n\n[*] Cancelado pelo usuário.")
    except Exception as e:
        print(f"\n[!] Erro: {e}")
        import traceback
        traceback.print_exc()

