const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');
const app = express();
// Aceita porta via variável de ambiente ou argumento, padrão 5001
const port = process.env.PORT || process.argv[2] || 5001;

app.use(express.json());

// Gerencia múltiplos clientes simultaneamente (um por user_id)
const clients = {}; // { user_id: { client, qrCodeData, isReady, reconnectAttempts, isReconnecting } }

let maxReconnectAttempts = 10; // Máximo de tentativas de reconexão
let reconnectDelay = 30000; // 30 segundos entre tentativas
let healthCheckInterval = null;

// Inicializa cliente para um user_id específico
function initClient(userId) {
    // Se não fornecido, usa porta (modo compatibilidade)
    if (!userId) {
        userId = `port_${port}`;
    }
    
    // Se já existe cliente para este user_id, não recria
    if (clients[userId] && clients[userId].client) {
        console.log(`[!] Cliente já existe para user_id ${userId}`);
        return;
    }
    // Configuração do Puppeteer (otimizado para gerar QR mais rápido)
    const puppeteerOptions = {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--disable-extensions',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-default-apps',
            '--disable-features=TranslateUI',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-sync',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain'
        ],
        timeout: 60000  // 60 segundos (reduzido para não travar)
    };

    // Tenta usar Chrome do sistema se disponível (macOS)
    const fs = require('fs');
    const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    if (fs.existsSync(chromePath)) {
        puppeteerOptions.executablePath = chromePath;
        console.log('✅ Usando Chrome do sistema');
    }

    // Usa clientId único baseado no user_id para separar sessões
    const clientId = `ylada_bot_user_${userId}`;
    const authPath = `.wwebjs_auth_user_${userId}`;
    const cachePath = `.wwebjs_cache_user_${userId}`;
    
    const client = new Client({
        authStrategy: new LocalAuth({
            clientId: clientId,
            dataPath: authPath // Mantém sessão persistente por user_id
        }),
        puppeteer: puppeteerOptions,
        webVersionCache: {
            type: 'local',
            path: cachePath // Cache da versão web por user_id
        }
    });
    
    // Inicializa estrutura para este user_id
    clients[userId] = {
        client: client,
        qrCodeData: null,
        isReady: false,
        reconnectAttempts: 0,
        isReconnecting: false,
        isConnecting: false, // Flag para rastrear se está no processo de conexão (QR escaneado)
        isAuthenticated: false // Flag para rastrear se está autenticado
    };

    client.on('qr', (qr) => {
        // NÃO gera novo QR Code se já está conectando ou autenticado
        if (clients[userId].isConnecting || clients[userId].isAuthenticated || clients[userId].isReady) {
            console.log(`[User ${userId}] ⚠️ QR Code solicitado mas já está conectando/autenticado. Ignorando...`);
            return;
        }
        
        console.log(`\n[User ${userId}] ═══════════════════════════════════════`);
        console.log(`[User ${userId}] 📱 QR CODE PARA CONECTAR WHATSAPP`);
        console.log(`[User ${userId}] ═══════════════════════════════════════\n`);
        clients[userId].qrCodeData = qr;
        clients[userId].isConnecting = false; // Reset flag quando gera novo QR
        qrcode.generate(qr, { small: true });
        console.log(`\n[User ${userId}] ═══════════════════════════════════════`);
        console.log(`[User ${userId}] Escaneie o QR Code acima com seu WhatsApp`);
        console.log(`[User ${userId}] Vá em: Configurações > Aparelhos conectados > Conectar um aparelho`);
        console.log(`[User ${userId}] ═══════════════════════════════════════\n`);
        console.log(`[User ${userId}] ✅ QR Code gerado e disponível na API /qr?user_id=${userId}`);
    });

    client.on('ready', () => {
        const timestamp = new Date().toISOString();
        console.log(`\n[${timestamp}] [User ${userId}] ═══════════════════════════════════════`);
        console.log(`[${timestamp}] [User ${userId}] ✅ WhatsApp CONECTADO E PRONTO!`);
        console.log(`[${timestamp}] [User ${userId}] ═══════════════════════════════════════`);
        console.log(`[${timestamp}] [User ${userId}] 📱 Sessão salva em: .wwebjs_auth_user_${userId}`);
        console.log(`[${timestamp}] [User ${userId}] ✅ Pronto para enviar e receber mensagens!`);
        console.log(`[${timestamp}] [User ${userId}] ═══════════════════════════════════════\n`);
        // FORÇA atualizar todas as flags imediatamente
        clients[userId].isReady = true;
        clients[userId].isAuthenticated = true;
        clients[userId].isConnecting = false; // Concluiu conexão
        clients[userId].qrCodeData = null;
        clients[userId].reconnectAttempts = 0;
        clients[userId].isReconnecting = false;
        // Log adicional para debug
        console.log(`[${timestamp}] [User ${userId}] 🔍 Flags após ready: isReady=${clients[userId].isReady}, isAuthenticated=${clients[userId].isAuthenticated}, isConnecting=${clients[userId].isConnecting}`);
    });

    client.on('authenticated', () => {
        const timestamp = new Date().toISOString();
        console.log(`\n[${timestamp}] [User ${userId}] ✅ Autenticado com sucesso!`);
        console.log(`[${timestamp}] [User ${userId}] ⏳ Aguardando inicialização completa...`);
        // authenticated não significa ready ainda, apenas que a autenticação foi aceita
        // Mas já pode considerar como conectando - remove QR Code para evitar confusão
        clients[userId].isAuthenticated = true; // Marca como autenticado
        clients[userId].isConnecting = true; // Ainda está conectando (aguardando ready)
        if (clients[userId].qrCodeData) {
            console.log(`[${timestamp}] [User ${userId}] 🧹 Removendo QR Code (já autenticado)`);
            clients[userId].qrCodeData = null;
        }
        
        // MELHORIA: Se o cliente já tem info, marca como ready imediatamente
        // Isso acelera a detecção de conexão
        if (clients[userId].client && clients[userId].client.info) {
            clients[userId].isReady = true;
            clients[userId].isConnecting = false;
            console.log(`[${timestamp}] [User ${userId}] ✅ Cliente já tem info! Marcando como ready imediatamente`);
        }
        
        console.log(`[${timestamp}] [User ${userId}] ✅ Flags após authenticated: isAuthenticated=true, isConnecting=${clients[userId].isConnecting}, isReady=${clients[userId].isReady}`);
    });

    client.on('auth_failure', (msg) => {
        const timestamp = new Date().toISOString();
        console.error(`\n[${timestamp}] [User ${userId}] ❌ Falha na autenticação:`, msg);
        console.error(`[${timestamp}] [User ${userId}] Detalhes:`, JSON.stringify(msg, null, 2));
        clients[userId].isReady = false;
        clients[userId].qrCodeData = null;
        
        // Se a falha foi por sessão inválida, limpa e permite nova tentativa
        if (msg && (msg.includes('SESSION') || msg.includes('session') || msg.includes('invalid'))) {
            console.log(`[${timestamp}] [User ${userId}] 🔄 Sessão inválida detectada. Limpando sessão...`);
            // Não limpa automaticamente, mas informa que precisa limpar manualmente
        }
    });

    client.on('disconnected', (reason) => {
        const timestamp = new Date().toISOString();
        console.log(`\n[${timestamp}] [User ${userId}] ⚠️ WhatsApp desconectado. Motivo: ${reason}`);
        console.log(`[${timestamp}] [User ${userId}] Tipo de desconexão: ${typeof reason}`);
        if (reason && typeof reason === 'object') {
            console.log(`[${timestamp}] [User ${userId}] Detalhes da desconexão:`, JSON.stringify(reason, null, 2));
        }
        clients[userId].isReady = false;
        clients[userId].qrCodeData = null;
        
        // Se foi desconectado por logout manual ou sessão removida, não tenta reconectar
        if (reason === 'LOGOUT' || (reason && reason.toString().includes('LOGOUT'))) {
            console.log(`[${timestamp}] [User ${userId}] 🚪 Logout manual detectado. Não tentará reconectar automaticamente.`);
            return;
        }
        
        // Tenta reconectar automaticamente
        if (!clients[userId].isReconnecting) {
            console.log(`[${timestamp}] [User ${userId}] 🔄 Tentando reconectar automaticamente...`);
            attemptReconnect(userId);
        }
    });

    client.on('loading_screen', (percent, message) => {
        console.log(`[User ${userId}] ⏳ Carregando: ${percent}% - ${message || 'Aguardando...'}`);
    });
    
    // Evento quando o QR Code é escaneado (mas ainda não autenticado)
    client.on('change_state', (state) => {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [User ${userId}] 🔄 Mudança de estado: ${state}`);
        
        if (state === 'CONNECTING' || state === 'OPENING' || state === 'PAIRING') {
            console.log(`[${timestamp}] [User ${userId}] 🔗 Estado: ${state} - QR Code foi escaneado!`);
            clients[userId].isConnecting = true; // Marca que está conectando
            clients[userId].isAuthenticated = false; // Ainda não autenticado, mas conectando
            // Remove QR Code IMEDIATAMENTE para evitar gerar novo durante conexão
            if (clients[userId].qrCodeData) {
                console.log(`[${timestamp}] [User ${userId}] 🧹 Removendo QR Code (foi escaneado, conectando...)`);
                clients[userId].qrCodeData = null;
            }
            console.log(`[${timestamp}] [User ${userId}] ✅ Flags atualizadas: isConnecting=true, isAuthenticated=false`);
            // IMPORTANTE: Força não gerar novo QR enquanto está conectando
            console.log(`[${timestamp}] [User ${userId}] 🚫 Bloqueando geração de novo QR Code enquanto isConnecting=true`);
        } else if (state === 'CONNECTED') {
            // Estado CONNECTED indica que está conectado
            console.log(`[${timestamp}] [User ${userId}] ✅ Estado CONNECTED detectado!`);
            clients[userId].isConnecting = false;
            clients[userId].isAuthenticated = true;
            // Força atualizar isReady se o cliente tem info
            if (clients[userId].client && clients[userId].client.info) {
                clients[userId].isReady = true;
                console.log(`[${timestamp}] [User ${userId}] ✅ Cliente marcado como ready (tem info)`);
            } else {
                // Se não tem info ainda, aguarda um pouco e verifica novamente
                setTimeout(() => {
                    if (clients[userId].client && clients[userId].client.info) {
                        clients[userId].isReady = true;
                        console.log(`[${timestamp}] [User ${userId}] ✅ Cliente marcado como ready (verificação tardia)`);
                    }
                }, 2000); // Aguarda 2 segundos para o cliente inicializar completamente
            }
            console.log(`[${timestamp}] [User ${userId}] ✅ Flags finais CONNECTED: isReady=${clients[userId].isReady}, isAuthenticated=true, isConnecting=false`);
        } else if (state === 'UNPAIRED' || state === 'UNPAIRED_IDLE') {
            console.log(`[${timestamp}] [User ${userId}] ⚠️ Dispositivo não pareado. Precisa escanear QR Code novamente.`);
            clients[userId].qrCodeData = null; // Força gerar novo QR
            clients[userId].isConnecting = false; // Reset flag
            clients[userId].isAuthenticated = false; // Reset flag
            console.log(`[${timestamp}] [User ${userId}] 🔄 Flags resetadas: isConnecting=false, isAuthenticated=false`);
        } else {
            // Outros estados (TIMEOUT, etc)
            console.log(`[${timestamp}] [User ${userId}] ℹ️ Estado recebido: ${state} (sem ação específica)`);
        }
    });

    // Log quando começa a inicializar
    console.log(`[User ${userId}] 🔄 Inicializando cliente WhatsApp...`);

    client.on('auth_failure', (msg) => {
        console.error(`[User ${userId}] ❌ Falha na autenticação:`, msg);
        clients[userId].isReady = false;
        clients[userId].qrCodeData = null;
    });

    // Listener para erros
    client.on('error', (error) => {
        const timestamp = new Date().toISOString();
        console.error(`[${timestamp}] [User ${userId}] ❌ Erro no cliente WhatsApp:`, error.message || error);
        
        // Se o erro indica desconexão, tenta reconectar
        if (error.message && (
            error.message.includes('disconnected') || 
            error.message.includes('Connection closed') ||
            error.message.includes('Session closed')
        )) {
            if (!clients[userId].isReconnecting && !clients[userId].isReady) {
                attemptReconnect(userId);
            }
        }
    });

    // Listener para mensagens recebidas
    client.on('message', async (msg) => {
        try {
            // Ignora mensagens próprias
            if (msg.fromMe) return;
            
            // Log da mensagem recebida
            const contact = await msg.getContact();
            const phone = msg.from.replace('@c.us', '').replace('@s.whatsapp.net', '');
            console.log(`\n[User ${userId}] [📨] Mensagem recebida de ${contact.pushname || phone}: ${msg.body}`);
            
            // Envia para webhook do Flask (se configurado)
            const webhookUrl = process.env.FLASK_WEBHOOK_URL || 'http://localhost:5002/webhook';
            
            try {
                await axios.post(webhookUrl, {
                    from: phone,
                    phone: phone,
                    body: msg.body,
                    message: msg.body,
                    timestamp: msg.timestamp * 1000,
                    user_id: userId // Adiciona user_id ao webhook
                }, {
                    timeout: 5000
                });
                console.log(`[User ${userId}] [✓] Mensagem enviada para webhook`);
            } catch (webhookError) {
                // Webhook não disponível ou erro - não é crítico
                console.log(`[User ${userId}] [!] Webhook não disponível (isso é normal se a IA não estiver configurada)`);
            }
        } catch (error) {
            console.error(`[User ${userId}] [!] Erro ao processar mensagem: ${error.message}`);
        }
    });

    client.initialize();
}

// Função para tentar reconectar automaticamente
function attemptReconnect(userId) {
    if (!clients[userId]) {
        return;
    }
    
    if (clients[userId].isReconnecting) {
        return; // Já está tentando reconectar
    }
    
    if (clients[userId].reconnectAttempts >= maxReconnectAttempts) {
        const timestamp = new Date().toISOString();
        console.error(`\n[${timestamp}] [User ${userId}] ❌ Máximo de tentativas de reconexão atingido (${maxReconnectAttempts}).`);
        console.error(`[${timestamp}] [User ${userId}] ⚠️ Por favor, verifique manualmente ou reinicie o servidor.`);
        clients[userId].isReconnecting = false;
        return;
    }
    
    clients[userId].isReconnecting = true;
    clients[userId].reconnectAttempts++;
    const timestamp = new Date().toISOString();
    const delaySeconds = reconnectDelay / 1000;
    
    console.log(`\n[${timestamp}] [User ${userId}] 🔄 Tentativa de reconexão ${clients[userId].reconnectAttempts}/${maxReconnectAttempts} em ${delaySeconds} segundos...`);
    
    setTimeout(() => {
        if (!clients[userId].isReady) {
            console.log(`[${new Date().toISOString()}] [User ${userId}] 🔄 Reconectando...`);
            try {
                // Destroi cliente antigo se existir
                if (clients[userId].client) {
                    clients[userId].client.destroy().catch(() => {});
                }
                // Remove cliente antigo
                delete clients[userId];
                // Cria novo cliente
                initClient(userId);
            } catch (error) {
                const timestamp = new Date().toISOString();
                console.error(`[${timestamp}] [User ${userId}] ❌ Erro ao tentar reconectar:`, error.message);
                clients[userId].isReconnecting = false;
                // Tenta novamente após delay
                setTimeout(() => {
                    clients[userId].isReconnecting = false;
                    attemptReconnect(userId);
                }, reconnectDelay);
            }
        } else {
            clients[userId].isReconnecting = false;
        }
    }, reconnectDelay);
}

// Health check periódico (verifica a cada 2 minutos se está conectado)
function startHealthCheck() {
    if (healthCheckInterval) {
        clearInterval(healthCheckInterval);
    }
    
    healthCheckInterval = setInterval(() => {
        const timestamp = new Date().toISOString();
        
        // Verifica cada cliente
        for (const userId in clients) {
            const clientData = clients[userId];
            if (!clientData) continue;
            
            // Verifica se deveria estar conectado mas não está
            if (!clientData.isReady && !clientData.qrCodeData && !clientData.isReconnecting) {
                console.log(`\n[${timestamp}] [User ${userId}] ⚠️ Health Check: WhatsApp não está conectado. Tentando reconectar...`);
                attemptReconnect(userId);
            } else if (clientData.isReady) {
                // Verifica se realmente está conectado (teste mais rigoroso)
                if (clientData.client && clientData.client.info) {
                    // Está OK
                } else {
                    console.log(`\n[${timestamp}] [User ${userId}] ⚠️ Health Check: Cliente marcado como pronto mas sem info. Reconectando...`);
                    clientData.isReady = false;
                    attemptReconnect(userId);
                }
            }
        }
    }, 120000); // Verifica a cada 2 minutos
}

// Rota raiz
app.get('/', (req, res) => {
    res.json({ 
        service: 'WhatsApp Web.js Server',
        status: 'running',
        ready: isReady,
        endpoints: {
            health: '/health',
            qr: '/qr',
            status: '/status',
            send: '/send (POST)',
            chats: '/chats',
            messages: '/chats/:chatId/messages'
        }
    });
});

// Rotas da API
app.get('/health', (req, res) => {
    const activeClients = Object.keys(clients).length;
    res.json({ status: 'ok', activeClients: activeClients });
});

app.get('/qr', (req, res) => {
    // Obtém user_id da query string (obrigatório em produção)
    const userId = req.query.user_id || req.query.userId;
    
    if (!userId) {
        // Modo compatibilidade: usa porta (para desenvolvimento)
        const requestedPort = req.query.port ? parseInt(req.query.port) : port;
        
        // Se a porta solicitada é diferente da atual, retorna erro claro
        if (requestedPort != port) {
            return res.status(503).json({ 
                error: `Servidor na porta ${port} não pode atender porta ${requestedPort}.`,
                hint: `Em produção, use user_id. Exemplo: /qr?user_id=3`,
                currentPort: port,
                requestedPort: requestedPort
            });
        }
        
        // Modo compatibilidade: usa user_id baseado na porta
        const compatUserId = `port_${port}`;
        if (!clients[compatUserId]) {
            initClient(compatUserId);
        }
        
        const clientData = clients[compatUserId];
        if (clientData.isReady) {
            return res.json({ ready: true, qr: null });
        }
        if (clientData.qrCodeData) {
            return res.json({ ready: false, qr: clientData.qrCodeData, hasQr: true });
        }
        return res.json({ ready: false, qr: null, hasQr: false });
    }
    
    // Inicializa cliente para este user_id se não existir
    if (!clients[userId]) {
        console.log(`[User ${userId}] Cliente não existe, inicializando...`);
        initClient(userId);
        // Aguarda um pouco para o cliente começar a inicializar
        // O QR code será gerado no evento 'qr'
        return res.json({ 
            ready: false, 
            qr: null, 
            hasQr: false,
            message: "Inicializando cliente... Aguarde alguns segundos e recarregue a página."
        });
    }
    
    const clientData = clients[userId];
    
    // PROTEÇÃO CRÍTICA: Se está conectando ou autenticado, NUNCA retorna QR Code
    if (clientData.isConnecting || clientData.isAuthenticated) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [User ${userId}] 🚫 QR Code solicitado mas isConnecting=${clientData.isConnecting} ou isAuthenticated=${clientData.isAuthenticated}. BLOQUEANDO geração de novo QR!`);
        return res.json({ 
            ready: clientData.isReady, 
            qr: null, 
            hasQr: false,
            isConnecting: clientData.isConnecting,
            isAuthenticated: clientData.isAuthenticated,
            message: clientData.isConnecting ? "QR Code foi escaneado, conectando..." : "Autenticado, aguardando inicialização..."
        });
    }
    
    // Se o cliente está sendo inicializado mas ainda não tem QR, aguarda
    if (clientData.client && !clientData.isReady && !clientData.qrCodeData && !clientData.isReconnecting) {
        console.log(`[User ${userId}] Cliente inicializando, aguardando QR code...`);
        return res.json({ 
            ready: false, 
            qr: null, 
            hasQr: false,
            message: "Aguardando geração do QR Code... Isso pode levar 10-30 segundos."
        });
    }
    
    if (clientData.isReady) {
        return res.json({ ready: true, qr: null, hasQr: false });
    }
    
    // ANTES de retornar QR, verifica novamente se não está conectando (proteção dupla)
    if (clientData.isConnecting || clientData.isAuthenticated) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [User ${userId}] 🚫 Tentativa de retornar QR mas isConnecting=${clientData.isConnecting}. BLOQUEANDO!`);
        return res.json({ 
            ready: false, 
            qr: null, 
            hasQr: false,
            isConnecting: clientData.isConnecting,
            isAuthenticated: clientData.isAuthenticated,
            message: "QR Code foi escaneado, conectando..."
        });
    }
    
    if (clientData.qrCodeData) {
        return res.json({ ready: false, qr: clientData.qrCodeData, hasQr: true });
    }
    
    // Se chegou aqui, algo está errado - tenta reinicializar
    console.log(`[User ${userId}] Cliente existe mas não tem estado válido, reinicializando...`);
    delete clients[userId];
    initClient(userId);
    return res.json({ 
        ready: false, 
        qr: null, 
        hasQr: false,
        message: "Reinicializando cliente... Aguarde alguns segundos e recarregue a página."
    });
});

app.post('/send', async (req, res) => {
    const userId = req.query.user_id || req.body.user_id || `port_${port}`;
    
    if (!clients[userId] || !clients[userId].isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        const { phone, message } = req.body;
        
        // Formata número
        let chatId = phone.replace(/\D/g, ''); // Remove caracteres não numéricos
        if (!chatId.includes('@c.us')) {
            chatId = chatId + '@c.us';
        }
        
        const result = await clients[userId].client.sendMessage(chatId, message);
        res.json({ success: true, messageId: result.id._serialized });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/status', async (req, res) => {
    const userId = req.query.user_id || req.query.userId || `port_${port}`;
    
    if (!clients[userId]) {
        return res.json({ 
            ready: false, 
            hasQr: false,
            actuallyConnected: false,
            clientInitialized: false,
            isAuthenticated: false
        });
    }
    
    const clientData = clients[userId];
    // Verifica se realmente está conectado tentando usar o cliente
    let actuallyReady = false;
    let clientInfo = null;
    let isAuthenticated = false;
    
    // Verifica se está autenticado (mesmo que não esteja ready ainda)
    if (clientData.client) {
        try {
            // Verifica se o cliente tem info (indica que está autenticado)
            if (clientData.client.info) {
                clientInfo = clientData.client.info;
                isAuthenticated = true;
                // Verifica se tem wid (WhatsApp ID) e se não está desconectado
                actuallyReady = !!(clientInfo.wid && !clientInfo.wid.includes('@temp'));
            }
        } catch (e) {
            // Ignora erro se não conseguir acessar info ainda
        }
    }
    
    // Se está ready, verifica novamente para garantir
    if (clientData.isReady && clientData.client) {
        try {
            // Verifica se o cliente está realmente conectado
            if (clientData.client.info) {
                clientInfo = clientData.client.info;
                // Verifica se tem wid (WhatsApp ID) e se não está desconectado
                actuallyReady = !!(clientInfo.wid && !clientInfo.wid.includes('@temp'));
            }
            
            // Verifica adicional se o cliente está realmente autenticado
            if (actuallyReady && clientData.client.pupBrowser) {
                // Tenta verificar se a página do Puppeteer ainda está aberta
                try {
                    const pages = await clientData.client.pupBrowser.pages();
                    if (!pages || pages.length === 0) {
                        actuallyReady = false;
                    }
                } catch (e) {
                    // Se não conseguir verificar, assume que está ok se tem info
                    // Não é crítico, apenas uma verificação adicional
                }
            }
        } catch (e) {
            actuallyReady = false;
            console.error(`[User ${userId}] Erro ao verificar conexão:`, e.message);
        }
    }
    
    // Extrai e formata número do telefone se disponível
    let phoneNumber = null;
    if (clientInfo && clientInfo.wid) {
        phoneNumber = clientInfo.wid;
        // Remove @c.us ou @s.whatsapp.net se houver
        phoneNumber = phoneNumber.replace('@c.us', '').replace('@s.whatsapp.net', '');
        // Formata número brasileiro (se começar com 55)
        if (phoneNumber.startsWith('55') && phoneNumber.length >= 12) {
            phoneNumber = `+${phoneNumber.substring(0, 2)} (${phoneNumber.substring(2, 4)}) ${phoneNumber.substring(4, 9)}-${phoneNumber.substring(9)}`;
        } else {
            phoneNumber = `+${phoneNumber}`;
        }
    }
    
    // MELHORIA: Verifica mais agressivamente se está conectado
    // Se está autenticado e não tem QR, considera conectado mesmo que não esteja ready ainda
    let finalConnected = actuallyReady || clientData.isReady; // PRIORIDADE: se isReady=true, está conectado
    const hasQrFlag = !!clientData.qrCodeData;
    const isAuthFlag = isAuthenticated || clientData.isAuthenticated;
    
    // Se isReady está true, FORÇA considerar conectado (mais confiável)
    if (clientData.isReady) {
        finalConnected = true;
        console.log(`[User ${userId}] ✅ Considerando conectado: isReady=true (mais confiável)`);
    } else if (!finalConnected && isAuthFlag && !hasQrFlag) {
        // Se está autenticado, sem QR, e tem cliente inicializado, considera conectado
        if (clientData.client && clientData.client.info) {
            finalConnected = true;
            console.log(`[User ${userId}] ✅ Considerando conectado: autenticado + sem QR + tem info`);
        }
    }
    
    res.json({ 
        ready: actuallyReady || clientData.isReady, 
        hasQr: hasQrFlag,
        actuallyConnected: finalConnected || actuallyReady || (isAuthFlag && !hasQrFlag), // Considera conectado se autenticado e sem QR
        clientInitialized: !!clientData.client,
        isAuthenticated: isAuthFlag, // Flag de autenticado
        isConnecting: clientData.isConnecting || false, // Flag de conectando (QR escaneado)
        phone_number: phoneNumber, // Adiciona número formatado
        clientInfo: clientInfo ? {
            wid: clientInfo.wid,
            pushname: clientInfo.pushname,
            platform: clientInfo.platform
        } : null,
        reconnectInfo: {
            attempts: clientData.reconnectAttempts,
            maxAttempts: maxReconnectAttempts,
            isReconnecting: clientData.isReconnecting,
            autoReconnectEnabled: true
        }
    });
});

// Desconecta o WhatsApp
app.post('/disconnect', async (req, res) => {
    const userId = req.query.user_id || req.body.user_id || `port_${port}`;
    
    try {
        if (!clients[userId] || !clients[userId].client) {
            return res.status(400).json({ error: 'Cliente não inicializado' });
        }
        
        // Desconecta o cliente
        await clients[userId].client.logout();
        clients[userId].isReady = false;
        clients[userId].qrCodeData = null;
        
        console.log(`[User ${userId}] ✅ WhatsApp desconectado com sucesso`);
        res.json({ success: true, message: 'WhatsApp desconectado com sucesso' });
    } catch (error) {
        console.error(`[User ${userId}] ❌ Erro ao desconectar:`, error);
        // Mesmo com erro, marca como desconectado
        if (clients[userId]) {
            clients[userId].isReady = false;
            clients[userId].qrCodeData = null;
        }
        res.json({ success: true, message: 'WhatsApp desconectado (pode ter havido um erro, mas foi desconectado)' });
    }
});

// Lista todas as conversas/chats do WhatsApp (melhorado)
app.get('/chats', async (req, res) => {
    const userId = req.query.user_id || req.query.userId || `port_${port}`;
    
    if (!clients[userId] || !clients[userId].isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        // Busca TODOS os chats (sem limite)
        const chats = await clients[userId].client.getChats();
        
        // Formata os chats com mais informações
        const formattedChats = await Promise.all(chats.map(async (chat) => {
            try {
                const contact = chat.contact || {};
                const lastMessage = chat.lastMessage || {};
                
                // Tenta obter mais informações do contato
                let contactName = contact.pushname || contact.name || chat.name || 'Sem nome';
                if (!contactName || contactName === 'Sem nome') {
                    try {
                        const contactInfo = await chat.getContact();
                        contactName = contactInfo.pushname || contactInfo.name || contactName;
                    } catch (e) {
                        // Ignora erro
                    }
                }
                
                return {
                    id: chat.id._serialized,
                    name: contactName,
                    phone: chat.id.user || '',
                    isGroup: chat.isGroup,
                    unreadCount: chat.unreadCount || 0,
                    lastMessage: lastMessage.body || (lastMessage.hasMedia ? '[Mídia]' : ''),
                    timestamp: lastMessage.timestamp ? lastMessage.timestamp * 1000 : (chat.timestamp ? chat.timestamp * 1000 : Date.now()),
                    pinned: chat.pinned || false,
                    isArchived: chat.archived || false
                };
            } catch (error) {
                // Se der erro em um chat específico, retorna dados básicos
                return {
                    id: chat.id._serialized,
                    name: chat.name || 'Sem nome',
                    phone: chat.id.user || '',
                    isGroup: chat.isGroup,
                    unreadCount: 0,
                    lastMessage: '',
                    timestamp: Date.now(),
                    pinned: false,
                    isArchived: false,
                    error: error.message
                };
            }
        }));
        
        // Ordena por última mensagem (mais recente primeiro)
        formattedChats.sort((a, b) => b.timestamp - a.timestamp);
        
        res.json({ 
            success: true, 
            chats: formattedChats,
            total: formattedChats.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Busca mensagens de um chat específico (melhorado com paginação)
app.get('/chats/:chatId/messages', async (req, res) => {
    const userId = req.query.user_id || req.query.userId || `port_${port}`;
    
    if (!clients[userId] || !clients[userId].isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        const { chatId } = req.params;
        const limit = parseInt(req.query.limit) || 100; // Aumentado padrão para 100
        const beforeId = req.query.before; // Para paginação
        
        // Busca o chat pelo ID
        const chat = await clients[userId].client.getChatById(chatId);
        
        // Busca mensagens do chat com opção de paginação
        let fetchOptions = { limit: Math.min(limit, 1000) }; // Limite máximo de 1000
        if (beforeId) {
            try {
                const beforeMsg = await clients[userId].client.getMessageById(beforeId);
                fetchOptions = { ...fetchOptions, before: beforeMsg };
            } catch (e) {
                // Se não encontrar mensagem, ignora paginação
            }
        }
        
        const messages = await chat.fetchMessages(fetchOptions);
        
        // Formata as mensagens
        const formattedMessages = messages.map(msg => {
            let contactName = null;
            
            // Se é mensagem de contato, extrai informações
            if (msg.type === 'contact' || msg.type === 'vcard') {
                if (msg.contact) {
                    // Tenta obter nome do contato
                    contactName = msg.contact.pushname || msg.contact.name || null;
                    
                    // Se não tem nome, tenta extrair do vCard no body
                    if (!contactName && msg.body) {
                        try {
                            const fnMatch = msg.body.match(/FN:([^\n\r;]+)/);
                            const nMatch = msg.body.match(/N:([^\n\r;]+)/);
                            if (fnMatch) {
                                contactName = fnMatch[1].trim();
                            } else if (nMatch) {
                                contactName = nMatch[1].split(';')[0].trim();
                            }
                        } catch (e) {
                            // Ignora erro
                        }
                    }
                } else if (msg.body) {
                    // Se não tem objeto contact, tenta extrair do body
                    try {
                        const fnMatch = msg.body.match(/FN:([^\n\r;]+)/);
                        const nMatch = msg.body.match(/N:([^\n\r;]+)/);
                        if (fnMatch) {
                            contactName = fnMatch[1].trim();
                        } else if (nMatch) {
                            contactName = nMatch[1].split(';')[0].trim();
                        }
                    } catch (e) {
                        // Ignora erro
                    }
                }
            }
            
            return {
                id: msg.id._serialized,
                body: msg.body || '',
                from: msg.from || chatId,
                fromMe: msg.fromMe,
                timestamp: msg.timestamp * 1000,
                type: msg.type,
                hasMedia: msg.hasMedia,
                mediaUrl: msg.hasMedia ? (msg.mediaUrl || '') : null,
                messageId: msg.id._serialized, // ID para baixar mídia
                contactName: contactName
            };
        });
        
        // Ordena por timestamp (mais antiga primeiro)
        formattedMessages.sort((a, b) => a.timestamp - b.timestamp);
        
        res.json({
            success: true,
            messages: formattedMessages,
            total: formattedMessages.length,
            hasMore: messages.length >= limit,
            nextCursor: formattedMessages.length > 0 ? formattedMessages[0].id : null
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Endpoint para baixar e servir mídias (imagens, áudios, vídeos)
app.get('/media/:messageId', async (req, res) => {
    const userId = req.query.user_id || req.query.userId || `port_${port}`;
    
    if (!clients[userId] || !clients[userId].isReady) {
        return res.status(400).json({ error: 'Cliente não conectado' });
    }
    
    try {
        const { messageId } = req.params;
        
        // Busca a mensagem pelo ID
        const message = await clients[userId].client.getMessageById(messageId);
        
        if (!message || !message.hasMedia) {
            return res.status(404).json({ error: 'Mídia não encontrada' });
        }
        
        // Baixa a mídia
        const media = await message.downloadMedia();
        
        if (!media) {
            return res.status(404).json({ error: 'Não foi possível baixar a mídia' });
        }
        
        // Converte base64 para buffer
        const buffer = Buffer.from(media.data, 'base64');
        
        // Define o tipo de conteúdo baseado no tipo de mídia
        let contentType = 'application/octet-stream';
        if (message.type === 'image') {
            contentType = media.mimetype || 'image/jpeg';
        } else if (message.type === 'audio' || message.type === 'ptt') {
            contentType = media.mimetype || 'audio/ogg; codecs=opus';
        } else if (message.type === 'video') {
            contentType = media.mimetype || 'video/mp4';
        } else if (message.type === 'document') {
            contentType = media.mimetype || 'application/pdf';
        }
        
        // Define headers
        res.setHeader('Content-Type', contentType);
        res.setHeader('Content-Length', buffer.length);
        res.setHeader('Cache-Control', 'public, max-age=31536000'); // Cache por 1 ano
        
        // Envia o buffer
        res.send(buffer);
    } catch (error) {
        console.error(`[User ${userId}] Erro ao baixar mídia:`, error);
        res.status(500).json({ error: error.message });
    }
});

// Inicia servidor
app.listen(port, () => {
    const timestamp = new Date().toISOString();
    console.log(`\n[${timestamp}] 🚀 Servidor WhatsApp Web.js rodando em http://localhost:${port}`);
    console.log(`[${timestamp}] 📱 Modo: Múltiplos usuários (suporta user_id)`);
    console.log(`[${timestamp}] 🔄 Auto-reconexão: ATIVADA (máx ${maxReconnectAttempts} tentativas)`);
    console.log(`[${timestamp}] 💚 Health Check: ATIVADO (verifica a cada 2 minutos)`);
    console.log(`[${timestamp}] ⚠️ Clientes serão inicializados sob demanda (quando /qr?user_id=X for chamado)\n`);
    
    // Inicia health check
    startHealthCheck();
    
    // Cleanup ao encerrar
    process.on('SIGINT', () => {
        console.log('\n⚠️ Encerrando servidor...');
        if (healthCheckInterval) {
            clearInterval(healthCheckInterval);
        }
        // Destroi todos os clientes
        for (const userId in clients) {
            if (clients[userId].client) {
                clients[userId].client.destroy().catch(() => {});
            }
        }
        process.exit(0);
    });
});

