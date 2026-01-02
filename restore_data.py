#!/usr/bin/env python3
"""
Script de Restore - BOT by YLADA
Restaura dados do backup
"""
import json
import os
import shutil
import zipfile
import sys
from datetime import datetime

def restore_data(backup_path_or_zip):
    """Restaura dados do backup"""
    
    print("🔄 Iniciando restauração dos dados...")
    
    # Verifica se é ZIP ou pasta
    if backup_path_or_zip.endswith('.zip'):
        # Extrai ZIP temporariamente
        extract_dir = f"temp_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(extract_dir, exist_ok=True)
        
        print(f"📦 Extraindo backup ZIP...")
        with zipfile.ZipFile(backup_path_or_zip, 'r') as zipf:
            zipf.extractall(extract_dir)
        
        # Encontra a pasta de backup dentro do ZIP
        backup_path = None
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path) and item.startswith('backup_'):
                backup_path = item_path
                break
        
        if not backup_path:
            # Se não encontrou pasta, usa o diretório extraído
            backup_path = extract_dir
        
        temp_dir = extract_dir
    else:
        backup_path = backup_path_or_zip
        temp_dir = None
    
    if not os.path.exists(backup_path):
        print(f"❌ Erro: Backup não encontrado em {backup_path}")
        return False
    
    print(f"📁 Restaurando de: {backup_path}")
    
    # Cria diretórios necessários
    os.makedirs("data", exist_ok=True)
    
    # 1. Restaura instâncias do usuário
    user_instances_backup = os.path.join(backup_path, "user_instances.json")
    if os.path.exists(user_instances_backup):
        shutil.copy2(user_instances_backup, "data/user_instances.json")
        print("✅ Instâncias do usuário restauradas")
    
    # 2. Restaura organizações
    organizations_backup = os.path.join(backup_path, "organizations.json")
    if os.path.exists(organizations_backup):
        shutil.copy2(organizations_backup, "data/organizations.json")
        print("✅ Organizações restauradas")
    
    # 3. Restaura sessões do WhatsApp
    sessions_backup = os.path.join(backup_path, "sessions")
    if os.path.exists(sessions_backup):
        if os.path.exists("data/sessions"):
            shutil.rmtree("data/sessions")
        shutil.copytree(sessions_backup, "data/sessions")
        print("✅ Sessões do WhatsApp restauradas")
    
    # 4. Restaura fluxos
    flows_files = [
        "flows.json",
        "flows_memory.json"
    ]
    for flows_file in flows_files:
        flows_backup = os.path.join(backup_path, flows_file)
        if os.path.exists(flows_backup):
            shutil.copy2(flows_backup, f"data/{flows_file}")
            print(f"✅ {flows_file} restaurado")
    
    # 4.1. Restaura pasta de fluxos
    flows_backup_dir = os.path.join(backup_path, "flows")
    if os.path.exists(flows_backup_dir):
        if os.path.exists("data/flows"):
            shutil.rmtree("data/flows")
        shutil.copytree(flows_backup_dir, "data/flows")
        print("✅ Pasta de fluxos restaurada")
    
    # 4.2. Restaura log de mensagens
    messages_log_backup = os.path.join(backup_path, "messages_log.json")
    if os.path.exists(messages_log_backup):
        shutil.copy2(messages_log_backup, "data/messages_log.json")
        print("✅ Log de mensagens restaurado")
    
    # 5. Restaura configurações
    config_files = [
        ".env",
        "config.json",
        "web/config.py"
    ]
    for config_file in config_files:
        backup_file = os.path.join(backup_path, os.path.basename(config_file))
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, config_file)
            print(f"✅ Configuração {os.path.basename(config_file)} restaurada")
    
    # 6. Mostra informações do backup
    backup_info_file = os.path.join(backup_path, "backup_info.json")
    if os.path.exists(backup_info_file):
        with open(backup_info_file, "r", encoding="utf-8") as f:
            backup_info = json.load(f)
            print(f"\n📋 Informações do backup:")
            print(f"   Data: {backup_info.get('date', 'N/A')}")
            print(f"   Arquivos: {len(backup_info.get('files_backed_up', []))}")
    
    # Limpa diretório temporário se foi criado
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Diretório temporário removido")
    
    print("\n✅ Restauração concluída com sucesso!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python3 restore_data.py <caminho_do_backup.zip ou pasta>")
        print("\nExemplo:")
        print("  python3 restore_data.py backups/backup_20241201_120000.zip")
        print("  python3 restore_data.py backups/backup_20241201_120000")
        sys.exit(1)
    
    backup_path = sys.argv[1]
    
    try:
        if restore_data(backup_path):
            print("\n✨ Dados restaurados! Você pode reiniciar o servidor agora.")
        else:
            print("\n❌ Erro ao restaurar dados")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao restaurar: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

