"""
Integração com WhatsApp usando WhatsApp Web.js (Node.js)
Solução GRATUITA e mais estável para múltiplas instâncias
"""
import subprocess
import json
import os
import time
import requests
from typing import Dict, Optional, List
from pathlib import Path


class WhatsAppWebJSHandler:
    """
    Handler usando WhatsApp Web.js via Node.js
    
    Esta solução é GRATUITA e permite múltiplas instâncias!
    Mais estável que Selenium/Playwright.
    """
    
    def __init__(self, instance_name: str = "default", port: int = 5001):
        """
        Inicializa handler
        
        Args:
            instance_name: Nome da instância (permite múltiplas)
            port: Porta do servidor Node.js
        """
        self.instance_name = instance_name
        self.port = port
        self.base_url = f"http://localhost:{port}"
        self.session_dir = Path("data/sessions") / instance_name
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.node_process = None
        self.is_connected = False
    
    def start_server(self) -> bool:
        """
        Inicia servidor Node.js com WhatsApp Web.js
        
        Returns:
            True se iniciado com sucesso
        """
        try:
            # Verifica se já está rodando
            try:
                response = requests.get(f"{self.base_url}/health", timeout=1)
                if response.status_code == 200:
                    print("[✓] Servidor já está rodando!")
                    return True
            except:
                pass
            
            # Verifica se Node.js está instalado
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("[!] Node.js não encontrado. Instale: https://nodejs.org")
                return False
            
            # Cria arquivo do servidor se não existir
            server_file = Path("whatsapp_server.js")
            if not server_file.exists():
                self._create_server_file(server_file)
            
            # Instala dependências se necessário
            if not Path("node_modules/whatsapp-web.js").exists():
                print("[*] Instalando dependências...")
                try:
                    subprocess.run(["npm", "install", "whatsapp-web.js", "qrcode-terminal", "express"], 
                                 check=True, timeout=60)
                except subprocess.TimeoutExpired:
                    print("[!] Timeout ao instalar dependências")
                    return False
            
            # Para processo anterior se existir
            if self.node_process:
                try:
                    self.node_process.terminate()
                    self.node_process.wait(timeout=2)
                except:
                    pass
            
            # Inicia servidor em background
            print(f"[*] Iniciando servidor WhatsApp Web.js na porta {self.port}...")
            self.node_process = subprocess.Popen(
                ["node", str(server_file)],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True  # Permite que continue rodando mesmo se o Python fechar
            )
            
            # Aguarda servidor iniciar (mais tempo para garantir)
            for i in range(10):  # Tenta por até 10 segundos
                time.sleep(1)
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print("[✓] Servidor WhatsApp Web.js iniciado!")
                        return True
                except:
                    pass
            
            print("[!] Servidor não respondeu após 10 segundos. Pode estar iniciando ainda...")
            return True  # Retorna True mesmo assim, pode estar gerando QR code
            
        except Exception as e:
            print(f"[!] Erro ao iniciar servidor: {e}")
            return False
    
    def _create_server_file(self, filepath: Path):
        """Cria arquivo do servidor Node.js"""
        # Usa o arquivo whatsapp_server.js se existir
        if Path("whatsapp_server.js").exists():
            # Copia o arquivo existente
            import shutil
            shutil.copy("whatsapp_server.js", filepath)
            print(f"[✓] Usando arquivo existente: whatsapp_server.js")
        else:
            # Cria novo arquivo
            server_code = f"""
const {{ Client, LocalAuth }} = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
const port = {self.port};

app.use(express.json());

let client = null;
let qrCodeData = null;
let isReady = false;

function initClient() {{
    client = new Client({{
        authStrategy: new LocalAuth({{
            clientId: '{self.instance_name}'
        }}),
        puppeteer: {{
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        }}
    }});

    client.on('qr', (qr) => {{
        console.log('\\n═══════════════════════════════════════');
        console.log('📱 QR CODE PARA CONECTAR WHATSAPP');
        console.log('═══════════════════════════════════════\\n');
        qrCodeData = qr;
        qrcode.generate(qr, {{ small: true }});
        console.log('\\nEscaneie o QR Code acima com seu WhatsApp\\n');
    }});

    client.on('ready', () => {{
        console.log('\\n✅ WhatsApp conectado!');
        isReady = true;
        qrCodeData = null;
    }});

    client.on('auth_failure', (msg) => {{
        console.error('❌ Falha na autenticação:', msg);
        isReady = false;
    }});

    client.on('disconnected', (reason) => {{
        console.log('⚠️ Desconectado:', reason);
        isReady = false;
    }});

    client.initialize();
}}

app.get('/health', (req, res) => {{
    res.json({{ status: 'ok', ready: isReady }});
}});

app.get('/qr', (req, res) => {{
    res.json({{ qr: qrCodeData, ready: isReady }});
}});

app.post('/send', async (req, res) => {{
    if (!isReady) {{
        return res.status(400).json({{ error: 'Cliente não conectado' }});
    }}
    try {{
        const {{ phone, message }} = req.body;
        let chatId = phone.replace(/\\D/g, '');
        if (!chatId.includes('@c.us')) {{
            chatId = chatId + '@c.us';
        }}
        const result = await client.sendMessage(chatId, message);
        res.json({{ success: true, messageId: result.id._serialized }});
    }} catch (error) {{
        res.status(500).json({{ error: error.message }});
    }}
}});

app.get('/status', (req, res) => {{
    res.json({{ ready: isReady, hasQr: !!qrCodeData }});
}});

app.listen(port, () => {{
    console.log(`\\n🚀 Servidor rodando em http://localhost:${{port}}\\n`);
    initClient();
}});
"""
            filepath.write_text(server_code, encoding="utf-8")
            print(f"[✓] Arquivo do servidor criado: {filepath}")
    
    def get_qr_code(self) -> Optional[str]:
        """Obtém QR Code para conexão"""
        try:
            response = requests.get(f"{self.base_url}/qr", timeout=5)
            data = response.json()
            return data.get("qr")
        except Exception as e:
            print(f"[!] Erro ao obter QR Code: {e}")
            return None
    
    def is_ready(self) -> bool:
        """Verifica se está conectado - verificação mais robusta"""
        try:
            # Primeiro verifica o status
            response = requests.get(f"{self.base_url}/status", timeout=2)
            data = response.json()
            is_ready_status = data.get("ready", False)
            
            # Se o status diz que está pronto, tenta verificar realmente tentando buscar chats
            if is_ready_status:
                try:
                    # Tenta buscar chats para confirmar que realmente está conectado
                    chats_response = requests.get(f"{self.base_url}/chats", timeout=3)
                    if chats_response.status_code == 200:
                        # Se conseguiu buscar chats, realmente está conectado
                        return True
                    else:
                        # Se não conseguiu, provavelmente não está conectado de verdade
                        print(f"[!] Status diz ready, mas /chats retornou {chats_response.status_code}")
                        return False
                except Exception as e:
                    # Se deu erro ao buscar chats, não está realmente conectado
                    print(f"[!] Status diz ready, mas erro ao verificar chats: {e}")
                    return False
            
            return False
        except Exception as e:
            print(f"[!] Erro ao verificar status: {e}")
            return False
    
    def send_message(self, phone: str, message: str) -> bool:
        """
        Envia mensagem
        
        Args:
            phone: Número (formato: 5511999999999)
            message: Mensagem
        
        Returns:
            True se enviado
        """
        if not self.is_ready():
            print("[!] WhatsApp não está conectado")
            return False
        
        try:
            response = requests.post(
                f"{self.base_url}/send",
                json={"phone": phone, "message": message},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"[✓] Mensagem enviada para {phone}")
                return True
            else:
                print(f"[!] Erro: {response.json()}")
                return False
        except Exception as e:
            print(f"[!] Erro ao enviar: {e}")
            return False
    
    def get_chats(self) -> List[Dict]:
        """
        Obtém lista de conversas/chats do WhatsApp
        
        Returns:
            Lista de chats formatados
        """
        if not self.is_ready():
            print("[!] WhatsApp não está conectado")
            return []
        
        try:
            response = requests.get(f"{self.base_url}/chats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("chats", [])
            else:
                print(f"[!] Erro ao buscar chats: {response.json()}")
                return []
        except Exception as e:
            print(f"[!] Erro ao buscar chats: {e}")
            return []
    
    def get_chat_messages(self, chat_id: str, limit: int = 50) -> List[Dict]:
        """
        Obtém mensagens de um chat específico
        
        Args:
            chat_id: ID do chat (formato: 5511999999999@c.us)
            limit: Número máximo de mensagens (padrão: 50)
        
        Returns:
            Lista de mensagens formatadas
        """
        if not self.is_ready():
            print("[!] WhatsApp não está conectado")
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/chats/{chat_id}/messages",
                params={"limit": limit},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("messages", [])
            else:
                print(f"[!] Erro ao buscar mensagens: {response.json()}")
                return []
        except Exception as e:
            print(f"[!] Erro ao buscar mensagens: {e}")
            return []
    
    def stop_server(self):
        """Para o servidor"""
        if self.node_process:
            self.node_process.terminate()
            self.node_process = None
            print("[*] Servidor parado")

