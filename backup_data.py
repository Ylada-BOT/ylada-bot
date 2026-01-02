#!/usr/bin/env python3
"""
Script de Backup - BOT by YLADA
Salva todos os dados importantes antes de reiniciar
"""
import json
import os
import shutil
from datetime import datetime
import zipfile

def backup_data():
    """Faz backup de todos os dados importantes"""
    
    print("🔄 Iniciando backup dos dados...")
    
    # Cria diretório de backup
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nome do arquivo de backup com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    os.makedirs(backup_path, exist_ok=True)
    
    print(f"📁 Criando backup em: {backup_path}")
    
    # 1. Backup de instâncias do usuário
    user_instances_file = "data/user_instances.json"
    if os.path.exists(user_instances_file):
        shutil.copy2(user_instances_file, os.path.join(backup_path, "user_instances.json"))
        print("✅ Instâncias do usuário salvas")
    
    # 2. Backup de organizações (se existir)
    organizations_file = "data/organizations.json"
    if os.path.exists(organizations_file):
        shutil.copy2(organizations_file, os.path.join(backup_path, "organizations.json"))
        print("✅ Organizações salvas")
    
    # 3. Backup de sessões do WhatsApp (se existir)
    sessions_dir = "data/sessions"
    if os.path.exists(sessions_dir):
        sessions_backup = os.path.join(backup_path, "sessions")
        shutil.copytree(sessions_dir, sessions_backup, dirs_exist_ok=True)
        print("✅ Sessões do WhatsApp salvas")
    
    # 4. Backup de fluxos (se existir arquivo)
    flows_files = [
        "data/flows.json",
        "data/flows_memory.json"
    ]
    for flows_file in flows_files:
        if os.path.exists(flows_file):
            shutil.copy2(flows_file, os.path.join(backup_path, os.path.basename(flows_file)))
            print(f"✅ {os.path.basename(flows_file)} salvo")
    
    # 4.1. Backup de pasta de fluxos
    flows_dir = "data/flows"
    if os.path.exists(flows_dir) and os.listdir(flows_dir):
        flows_backup = os.path.join(backup_path, "flows")
        shutil.copytree(flows_dir, flows_backup, dirs_exist_ok=True)
        print("✅ Pasta de fluxos salva")
    
    # 4.2. Backup de logs de mensagens
    messages_log = "data/messages_log.json"
    if os.path.exists(messages_log):
        shutil.copy2(messages_log, os.path.join(backup_path, "messages_log.json"))
        print("✅ Log de mensagens salvo")
    
    # 5. Backup de configurações
    config_files = [
        ".env",
        "config.json",
        "web/config.py"
    ]
    for config_file in config_files:
        if os.path.exists(config_file):
            dest = os.path.join(backup_path, os.path.basename(config_file))
            shutil.copy2(config_file, dest)
            print(f"✅ Configuração {os.path.basename(config_file)} salva")
    
    # 6. Cria arquivo de informações do backup
    backup_info = {
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "files_backed_up": []
    }
    
    # Lista arquivos no backup
    for root, dirs, files in os.walk(backup_path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), backup_path)
            backup_info["files_backed_up"].append(rel_path)
    
    with open(os.path.join(backup_path, "backup_info.json"), "w", encoding="utf-8") as f:
        json.dump(backup_info, f, indent=2, ensure_ascii=False)
    
    # 7. Cria ZIP do backup
    zip_path = f"{backup_path}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_path)
                zipf.write(file_path, arcname)
    
    print(f"\n✅ Backup completo criado!")
    print(f"📦 Arquivo ZIP: {zip_path}")
    print(f"📁 Pasta: {backup_path}")
    print(f"\n💾 Tamanho do backup: {os.path.getsize(zip_path) / 1024 / 1024:.2f} MB")
    
    return backup_path, zip_path

if __name__ == "__main__":
    try:
        backup_path, zip_path = backup_data()
        print("\n✨ Backup concluído com sucesso!")
        print(f"\n📋 Para restaurar depois, execute:")
        print(f"   python3 restore_data.py {zip_path}")
    except Exception as e:
        print(f"\n❌ Erro ao fazer backup: {e}")
        import traceback
        traceback.print_exc()

