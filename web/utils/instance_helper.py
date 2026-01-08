"""
Helper para gerenciar instância única por usuário
No modo simplificado: 1 usuário = 1 instância WhatsApp
"""
import json
import os
import subprocess
import time
import requests
from datetime import datetime
from pathlib import Path
from web.utils.auth_helpers import get_current_user_id


def get_or_create_user_instance(user_id=None):
    """
    Obtém ou cria automaticamente a instância do usuário
    
    No modo simplificado: cada usuário tem apenas 1 instância
    Se não existir, cria automaticamente
    
    Returns:
        dict: Dados da instância do usuário
    """
    if not user_id:
        user_id = get_current_user_id() or 1  # Default para desenvolvimento
    
    # MODO SIMPLES: Usa arquivo JSON
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    os.makedirs(os.path.dirname(instances_file), exist_ok=True)
    
    # Carrega instâncias existentes
    user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                user_instances = json.load(f)
        except:
            user_instances = {}
    
    # Verifica se usuário já tem instância
    user_key = str(user_id)
    if user_key in user_instances:
        return user_instances[user_key]
    
    # Cria nova instância para o usuário
    # Calcula porta baseada no user_id (5001, 5002, 5003...)
    base_port = 5001 + (user_id - 1)
    
    new_instance = {
        'id': user_id,  # ID da instância = ID do usuário (simplificado)
        'user_id': user_id,
        'name': f'Meu WhatsApp',
        'status': 'disconnected',
        'port': base_port,
        'phone_number': None,
        'agent_id': None,
        'messages_sent': 0,
        'messages_received': 0,
        'created_at': datetime.now().isoformat(),
        'session_dir': f"data/sessions/user_{user_id}"
    }
    
    # Salva instância
    user_instances[user_key] = new_instance
    with open(instances_file, 'w', encoding='utf-8') as f:
        json.dump(user_instances, f, indent=2, ensure_ascii=False)
    
    return new_instance


def get_user_instance_id(user_id=None):
    """
    Obtém ID da instância do usuário
    
    Returns:
        int: ID da instância do usuário
    """
    instance = get_or_create_user_instance(user_id)
    return instance.get('id')


def update_user_instance(user_id, updates):
    """
    Atualiza dados da instância do usuário
    
    Args:
        user_id: ID do usuário
        updates: Dict com campos para atualizar
    """
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    
    user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                user_instances = json.load(f)
        except:
            user_instances = {}
    
    user_key = str(user_id)
    if user_key in user_instances:
        user_instances[user_key].update(updates)
        user_instances[user_key]['updated_at'] = datetime.now().isoformat()
        
        with open(instances_file, 'w', encoding='utf-8') as f:
            json.dump(user_instances, f, indent=2, ensure_ascii=False)


def get_whatsapp_server_url(port=None):
    """
    Retorna a URL do servidor WhatsApp baseada no ambiente.
    
    Args:
        port: Porta do servidor (opcional, usa padrão se não fornecido)
        
    Returns:
        str: URL do servidor WhatsApp
    """
    from config.settings import WHATSAPP_SERVER_URL, WHATSAPP_SERVER_PORT, IS_PRODUCTION
    
    if port is None:
        port = WHATSAPP_SERVER_PORT
    
    # Se está em produção e WHATSAPP_SERVER_URL está configurado
    if IS_PRODUCTION and WHATSAPP_SERVER_URL and 'localhost' not in WHATSAPP_SERVER_URL:
        # Em produção, cada porta precisa de um serviço separado
        # Ou usar o mesmo serviço com roteamento interno
        # Por enquanto, usa a URL base e passa porta como parâmetro
        base_url = WHATSAPP_SERVER_URL.rstrip('/')
        # Remove porta da URL se existir
        if ':' in base_url.split('//')[-1].split('/')[0]:
            # Extrai apenas o domínio sem porta
            parts = base_url.split('//')
            domain = parts[-1].split('/')[0]
            if ':' in domain:
                domain = domain.split(':')[0]
            base_url = f"{parts[0]}//{domain}"
        return base_url
    
    # Caso contrário, usa localhost (desenvolvimento)
    return f"http://localhost:{port}"

def ensure_whatsapp_server_running(port):
    """
    Garante que o servidor Node.js WhatsApp está rodando na porta especificada.
    Se não estiver, inicia automaticamente.
    
    Args:
        port: Porta do servidor Node.js
        
    Returns:
        bool: True se servidor está rodando ou foi iniciado com sucesso
    """
    from config.settings import IS_PRODUCTION
    
    # Em produção, não tenta iniciar servidor automaticamente
    if IS_PRODUCTION:
        server_url = get_whatsapp_server_url(port)
        try:
            response = requests.get(f"{server_url}/health", timeout=2)
            if response.status_code == 200:
                print(f"[✓] Servidor WhatsApp está rodando em {server_url}")
                return True
        except:
            print(f"[!] Servidor WhatsApp não está acessível em {server_url}")
            return False
    
    # Verifica se já está rodando
    try:
        server_url = get_whatsapp_server_url(port)
        response = requests.get(f"{server_url}/health", timeout=2)
        if response.status_code == 200:
            print(f"[✓] Servidor WhatsApp já está rodando em {server_url}")
            return True
    except requests.exceptions.ConnectionError:
        print(f"[!] Servidor não está rodando em {server_url}, tentando iniciar...")
    except Exception as e:
        print(f"[!] Erro ao verificar porta {port}: {e}")
    
    # Se não está rodando, tenta iniciar
    try:
        # Verifica se Node.js está instalado
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print(f"[!] Node.js não encontrado. Instale: https://nodejs.org")
            return False
        
        # Verifica se o arquivo whatsapp_server.js existe
        server_file = Path("whatsapp_server.js")
        if not server_file.exists():
            print(f"[!] Arquivo whatsapp_server.js não encontrado")
            return False
        
        # Verifica se já existe um processo rodando na porta
        try:
            # Tenta matar processo antigo na porta (se houver)
            if os.name == 'posix':  # Unix/Linux/macOS
                # Busca processos na porta
                result = subprocess.run(
                    ["lsof", "-ti", f":{port}"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                # Se encontrou processo, mata
                if result.returncode == 0 and result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            try:
                                subprocess.run(
                                    ["kill", "-9", pid],
                                    capture_output=True,
                                    check=False,
                                    timeout=2
                                )
                            except:
                                pass
        except:
            pass
        
        # Inicia servidor em background
        print(f"[*] Iniciando servidor WhatsApp na porta {port}...")
        env = os.environ.copy()
        env['PORT'] = str(port)
        
        # Cria arquivo de log para esta porta
        log_file = f"/tmp/whatsapp_server_{port}.log"
        
        # Inicia processo em background com redirecionamento de saída
        try:
            # Usa nohup ou start_new_session para garantir que o processo persista
            log_handle = open(log_file, 'a')
            process = subprocess.Popen(
                ["node", "whatsapp_server.js", str(port)],
                env=env,
                stdout=log_handle,
                stderr=log_handle,
                cwd=os.getcwd(),
                start_new_session=True,  # Permite que o processo continue após o Flask
                preexec_fn=os.setsid if os.name == 'posix' else None  # Cria novo grupo de processos no Unix
            )
            # Não fecha o handle imediatamente, deixa o processo gerenciar
            # O handle será fechado quando o processo terminar
        except Exception as e:
            print(f"[!] Erro ao iniciar processo: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Aguarda alguns segundos para o servidor iniciar (aumentado para 5 segundos)
        print(f"[*] Aguardando inicialização do servidor na porta {port}...")
        time.sleep(5)
        
        # Verifica se está rodando (tenta até 3 vezes)
        for attempt in range(3):
            try:
                response = requests.get(f"http://localhost:{port}/health", timeout=3)
                if response.status_code == 200:
                    print(f"[✓] Servidor WhatsApp iniciado com sucesso na porta {port}")
                    return True
            except requests.exceptions.ConnectionError:
                if attempt < 2:
                    print(f"[*] Tentativa {attempt + 1}/3: Aguardando servidor na porta {port}...")
                    time.sleep(2)
                else:
                    print(f"[!] Servidor não respondeu após 3 tentativas na porta {port}")
            except Exception as e:
                print(f"[!] Erro ao verificar servidor na porta {port}: {e}")
        
        # Se não respondeu, verifica se o processo ainda está rodando
        if process.poll() is None:
            print(f"[✓] Processo Node.js está rodando na porta {port}, mas servidor ainda não respondeu")
            print(f"[*] Verifique o log: tail -f {log_file}")
            return True
        else:
            # Processo terminou, verifica o log
            print(f"[!] Processo Node.js terminou na porta {port}")
            print(f"[*] Verifique o log para erros: tail -20 {log_file}")
            try:
                with open(log_file, 'r') as f:
                    last_lines = f.readlines()[-10:]
                    if last_lines:
                        print(f"[*] Últimas linhas do log:")
                        for line in last_lines:
                            print(f"    {line.strip()}")
            except:
                pass
            return False
            
    except Exception as e:
        print(f"[!] Erro ao iniciar servidor WhatsApp na porta {port}: {e}")
        return False









