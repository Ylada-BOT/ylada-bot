"""
Helper para gerenciar múltiplas instâncias por usuário
Agora suporta: 1 usuário = múltiplas instâncias WhatsApp
"""
import json
import os
import subprocess
import time
import requests
from datetime import datetime
from pathlib import Path
from web.utils.auth_helpers import get_current_user_id


def get_user_instances(user_id=None):
    """
    Obtém todas as instâncias do usuário
    
    Returns:
        list: Lista de instâncias do usuário
    """
    if not user_id:
        user_id = get_current_user_id() or 1
    
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    os.makedirs(os.path.dirname(instances_file), exist_ok=True)
    
    # Carrega instâncias existentes
    all_user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                all_user_instances = json.load(f)
        except:
            all_user_instances = {}
    
    user_key = str(user_id)
    
    # Verifica formato antigo (compatibilidade)
    if user_key in all_user_instances:
        user_data = all_user_instances[user_key]
        # Se é formato antigo (instância única), converte para novo formato
        if 'instances' not in user_data:
            old_instance = user_data if isinstance(user_data, dict) and 'id' in user_data else None
            if old_instance:
                # Converte para novo formato
                all_user_instances[user_key] = {
                    'instances': [old_instance],
                    'default_instance_id': old_instance.get('id', user_id)
                }
                with open(instances_file, 'w', encoding='utf-8') as f:
                    json.dump(all_user_instances, f, indent=2, ensure_ascii=False)
                return all_user_instances[user_key].get('instances', [])
    
    # Retorna instâncias do usuário
    if user_key in all_user_instances:
        return all_user_instances[user_key].get('instances', [])
    
    return []


def get_or_create_user_instance(user_id=None, instance_id=None):
    """
    Obtém ou cria uma instância do usuário
    
    Se instance_id não for fornecido, retorna a primeira instância ou cria uma nova
    
    Args:
        user_id: ID do usuário
        instance_id: ID da instância específica (opcional)
    
    Returns:
        dict: Dados da instância do usuário
    """
    if not user_id:
        user_id = get_current_user_id() or 1
    
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    os.makedirs(os.path.dirname(instances_file), exist_ok=True)
    
    # Carrega instâncias existentes
    all_user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                all_user_instances = json.load(f)
        except:
            all_user_instances = {}
    
    user_key = str(user_id)
    
    # Verifica formato antigo (compatibilidade)
    if user_key in all_user_instances:
        user_data = all_user_instances[user_key]
        if 'instances' not in user_data:
            # Formato antigo - converte
            old_instance = user_data if isinstance(user_data, dict) and 'id' in user_data else None
            if old_instance:
                all_user_instances[user_key] = {
                    'instances': [old_instance],
                    'default_instance_id': old_instance.get('id', user_id)
                }
                with open(instances_file, 'w', encoding='utf-8') as f:
                    json.dump(all_user_instances, f, indent=2, ensure_ascii=False)
    
    # Inicializa estrutura do usuário se não existir
    if user_key not in all_user_instances:
        all_user_instances[user_key] = {
            'instances': [],
            'default_instance_id': None
        }
    
    user_instances = all_user_instances[user_key].get('instances', [])
    
    # Se instance_id foi fornecido, busca essa instância específica
    if instance_id:
        for inst in user_instances:
            if inst.get('id') == instance_id:
                return inst
        # Se não encontrou, retorna None (instância não existe)
        return None
    
    # Se não forneceu instance_id, retorna primeira instância ou cria nova
    if user_instances:
        # Retorna primeira instância (ou pode usar default_instance_id se configurado)
        default_id = all_user_instances[user_key].get('default_instance_id')
        if default_id:
            for inst in user_instances:
                if inst.get('id') == default_id:
                    return inst
        return user_instances[0]
    
    # Cria nova instância se não existir nenhuma
    from config.settings import IS_PRODUCTION, WHATSAPP_SERVER_PORT
    if IS_PRODUCTION:
        base_port = WHATSAPP_SERVER_PORT  # Todos usam a mesma porta em produção
    else:
        # Em desenvolvimento, TODAS as instâncias usam a mesma porta (5001)
        # O servidor WhatsApp gerencia múltiplos clientes usando user_id único
        base_port = WHATSAPP_SERVER_PORT  # Sempre 5001 em desenvolvimento
    
    # Gera novo ID de instância
    max_id = 0
    for inst in user_instances:
        max_id = max(max_id, inst.get('id', 0))
    new_instance_id = max_id + 1
    
    new_instance = {
        'id': new_instance_id,
        'user_id': user_id,
        'name': f'WhatsApp {new_instance_id}',
        'status': 'disconnected',
        'port': base_port,
        'phone_number': None,
        'agent_id': None,
        'messages_sent': 0,
        'messages_received': 0,
        'created_at': datetime.now().isoformat(),
        'session_dir': f"data/sessions/user_{user_id}_instance_{new_instance_id}"
    }
    
    # Adiciona instância
    user_instances.append(new_instance)
    all_user_instances[user_key]['instances'] = user_instances
    if not all_user_instances[user_key].get('default_instance_id'):
        all_user_instances[user_key]['default_instance_id'] = new_instance_id
    
    # Salva
    with open(instances_file, 'w', encoding='utf-8') as f:
        json.dump(all_user_instances, f, indent=2, ensure_ascii=False)
    
    return new_instance


def get_user_instance_id(user_id=None, instance_id=None):
    """
    Obtém ID da instância do usuário
    
    Args:
        user_id: ID do usuário
        instance_id: ID da instância específica (opcional)
    
    Returns:
        int: ID da instância do usuário
    """
    instance = get_or_create_user_instance(user_id, instance_id)
    if instance:
        return instance.get('id')
    return None


def create_user_instance(user_id=None, name=None):
    """
    Cria uma nova instância para o usuário
    
    Args:
        user_id: ID do usuário
        name: Nome da instância (opcional)
    
    Returns:
        dict: Dados da nova instância criada
    """
    if not user_id:
        user_id = get_current_user_id() or 1
    
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    os.makedirs(os.path.dirname(instances_file), exist_ok=True)
    
    # Carrega instâncias existentes
    all_user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                all_user_instances = json.load(f)
        except:
            all_user_instances = {}
    
    user_key = str(user_id)
    
    # Inicializa estrutura do usuário se não existir
    if user_key not in all_user_instances:
        all_user_instances[user_key] = {
            'instances': [],
            'default_instance_id': None
        }
    
    user_instances = all_user_instances[user_key].get('instances', [])
    
    # Encontra próxima porta disponível
    from config.settings import IS_PRODUCTION
    used_ports = set()
    for user_data in all_user_instances.values():
        for inst in user_data.get('instances', []):
            used_ports.add(inst.get('port', 5001))
    
    if IS_PRODUCTION:
        base_port = 5001  # Todos usam a mesma porta em produção
    else:
        base_port = 5001
        while base_port in used_ports:
            base_port += 1
    
    # Gera novo ID de instância
    max_id = 0
    for inst in user_instances:
        max_id = max(max_id, inst.get('id', 0))
    new_instance_id = max_id + 1
    
    if not name:
        name = f'WhatsApp {new_instance_id}'
    
    new_instance = {
        'id': new_instance_id,
        'user_id': user_id,
        'name': name,
        'status': 'disconnected',
        'port': base_port,
        'phone_number': None,
        'agent_id': None,
        'messages_sent': 0,
        'messages_received': 0,
        'created_at': datetime.now().isoformat(),
        'session_dir': f"data/sessions/user_{user_id}_instance_{new_instance_id}"
    }
    
    # Adiciona instância
    user_instances.append(new_instance)
    all_user_instances[user_key]['instances'] = user_instances
    
    # Salva
    with open(instances_file, 'w', encoding='utf-8') as f:
        json.dump(all_user_instances, f, indent=2, ensure_ascii=False)
    
    return new_instance


def get_instance_user_id(user_id, instance_id):
    """
    Gera identificador único para instância no servidor WhatsApp
    Formato: user_id_instance_id (ex: "2_1", "2_2")
    
    Isso permite que o mesmo usuário tenha múltiplas instâncias funcionando independentemente
    
    Args:
        user_id: ID do usuário
        instance_id: ID da instância
    
    Returns:
        str: Identificador único (ex: "2_1")
    """
    return f"{user_id}_{instance_id}"


def update_user_instance(user_id, instance_id, updates):
    """
    Atualiza dados da instância do usuário
    
    Args:
        user_id: ID do usuário
        instance_id: ID da instância
        updates: Dict com campos para atualizar
    """
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    
    all_user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                all_user_instances = json.load(f)
        except:
            all_user_instances = {}
    
    user_key = str(user_id)
    if user_key in all_user_instances:
        instances = all_user_instances[user_key].get('instances', [])
        for inst in instances:
            if inst.get('id') == instance_id:
                inst.update(updates)
                inst['updated_at'] = datetime.now().isoformat()
                all_user_instances[user_key]['instances'] = instances
                with open(instances_file, 'w', encoding='utf-8') as f:
                    json.dump(all_user_instances, f, indent=2, ensure_ascii=False)
                return


def get_whatsapp_server_url(port=None):
    """
    Retorna a URL do servidor WhatsApp baseada no ambiente.
    
    Args:
        port: Porta do servidor (opcional, usa padrão se não fornecido)
        
    Returns:
        str: URL do servidor WhatsApp (sempre com protocolo)
    """
    import os
    from config.settings import WHATSAPP_SERVER_URL, WHATSAPP_SERVER_PORT, IS_PRODUCTION
    
    if port is None:
        port = WHATSAPP_SERVER_PORT
    
    # PRIORIDADE 1: Se está no Railway, SEMPRE usa comunicação interna (nome do serviço)
    # Isso garante que mesmo se WHATSAPP_SERVER_URL estiver configurada com URL pública,
    # ainda usará comunicação interna (mais rápida e confiável)
    if IS_PRODUCTION and os.getenv('RAILWAY_ENVIRONMENT'):
        # No Railway, serviços se comunicam via nome do serviço usando HTTP interno
        # Tenta detectar nome do serviço WhatsApp de várias formas:
        
        # 1. Variável de ambiente explícita
        service_name = os.getenv('WHATSAPP_SERVICE_NAME')
        
        # 2. Se WHATSAPP_SERVER_URL está configurada com URL do Railway, extrai nome do serviço
        if not service_name and WHATSAPP_SERVER_URL and 'railway.app' in WHATSAPP_SERVER_URL:
            # Extrai nome do serviço da URL (ex: https://whatsapp-server-2-production.up.railway.app -> whatsapp-server-2)
            url_parts = WHATSAPP_SERVER_URL.replace('https://', '').replace('http://', '').split('.')
            if url_parts:
                service_name = url_parts[0]  # Primeira parte antes do primeiro ponto
        
        # 3. Fallback para nome padrão
        if not service_name:
            service_name = 'whatsapp-server-2'
        
        # Railway usa comunicação interna via nome do serviço (HTTP, não HTTPS)
        return f"http://{service_name}:{port}"
    
    # PRIORIDADE 2: Se WHATSAPP_SERVER_URL está configurado e não é localhost (outros ambientes)
    if IS_PRODUCTION and WHATSAPP_SERVER_URL and 'localhost' not in WHATSAPP_SERVER_URL:
        base_url = WHATSAPP_SERVER_URL.strip().rstrip('/')
        
        # Se a URL já começa com http:// ou https://, usa como está
        if base_url.startswith('http://') or base_url.startswith('https://'):
            return base_url.rstrip('/')
        
        # Se não tem protocolo, adiciona https:// (assume público)
        if not base_url.startswith('http://') and not base_url.startswith('https://'):
            return f"https://{base_url}"
        
        return base_url.rstrip('/')
    
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
            # Tenta health check primeiro
            health_url = f"{server_url}/health" if '/health' not in server_url else server_url
            response = requests.get(health_url, timeout=3)
            if response.status_code == 200:
                print(f"[✓] Servidor WhatsApp está rodando em {server_url}")
                return True
        except requests.exceptions.ConnectionError:
            print(f"[!] Servidor WhatsApp não está acessível em {server_url} (porta {port})")
            print(f"[!] Em produção, cada porta precisa de um serviço Node.js separado no Railway")
            return False
        except Exception as e:
            print(f"[!] Erro ao verificar servidor WhatsApp: {e}")
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









