const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const axios = require('axios');
const app = express();
// Aceita porta via variável de ambiente ou argumento, padrão 5001
const port = process.env.PORT || process.argv[2] || 5001;

app.use(express.json());

let client = null;
let qrCodeData = null;
let isReady = false;
let reconnectAttempts = 0;
let maxReconnectAttempts = 10; // Máximo de tentativas de reconexão
let reconnectDelay = 30000; // 30 segundos entre tentativas
let isReconnecting = false;
let healthCheckInterval = null;

// Inicializa cliente
function initClient() {
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

    // Usa clientId único baseado na porta para separar sessões
    const clientId = `ylada_bot_${port}`;
    const authPath = `.wwebjs_auth_${port}`;
    const cachePath = `.wwebjs_cache_${port}`;
    
    client = new Client({
        authStrategy: new LocalAuth({
            clientId: clientId,
            dataPath: authPath // Mantém sessão persistente por porta
        }),
        puppeteer: puppeteerOptions,
        webVersionCache: {
            type: 'local',
            path: cachePath // Cache da versão web por porta
        }
    });

    client.on('qr', (qr) => {
        console.log('\n═══════════════════════════════════════');
        console.log('📱 QR CODE PARA CONECTAR WHATSAPP');
        console.log('═══════════════════════════════════════\n');
        qrCodeData = qr;
        qrcode.generate(qr, { small: true });
        console.log('\n═══════════════════════════════════════');
        console.log('Escaneie o QR Code acima com seu WhatsApp');
        console.log('Vá em: Configurações > Aparelhos conectados > Conectar um aparelho');
        console.log('═══════════════════════════════════════\n');
        console.log('✅ QR Code gerado e disponível na API /qr');
    });

    client.on('ready', () => {
        const timestamp = new Date().toISOString();
        console.log(`\n[${timestamp}] ✅ WhatsApp conectado com sucesso!`);
        isReady = true;
        qrCodeData = null;
        reconnectAttempts = 0; // Reset contador de tentativas
        isReconnecting = false;
    });

    client.on('authenticated', () => {
        console.log('✅ Autenticado!');
    });

    client.on('auth_failure', (msg) => {
        console.error('❌ Falha na autenticação:', msg);
        isReady = false;
    });

    client.on('disconnected', (reason) => {
        const timestamp = new Date().toISOString();
        console.log(`\n[${timestamp}] ⚠️ WhatsApp desconectado. Motivo: ${reason}`);
        isReady = false;
        qrCodeData = null;
        
        // Tenta reconectar automaticamente (exceto se foi logout manual)
        if (reason !== 'LOGOUT' && !isReconnecting) {
            attemptReconnect();
        }
    });

    client.on('loading_screen', (percent, message) => {
        console.log(`⏳ Carregando: ${percent}% - ${message}`);
    });

    // Log quando começa a inicializar
    console.log('🔄 Inicializando cliente WhatsApp...');

    client.on('auth_failure', (msg) => {
        console.error('❌ Falha na autenticação:', msg);
        isReady = false;
        qrCodeData = null;
    });

    // Listener para erros
    client.on('error', (error) => {
        const timestamp = new Date().toISOString();
        console.error(`[${timestamp}] ❌ Erro no cliente WhatsApp:`, error.message || error);
        
        // Se o erro indica desconexão, tenta reconectar
        if (error.message && (
            error.message.includes('disconnected') || 
            error.message.includes('Connection closed') ||
            error.message.includes('Session closed')
        )) {
            if (!isReconnecting && !isReady) {
                attemptReconnect();
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
            console.log(`\n[📨] Mensagem recebida de ${contact.pushname || phone}: ${msg.body}`);
            
            // Envia para webhook do Flask (se configurado)
            const webhookUrl = process.env.FLASK_WEBHOOK_URL || 'http://localhost:5002/webhook';
            
            try {
                await axios.post(webhookUrl, {
                    from: phone,
                    phone: phone,
                    body: msg.body,
                    message: msg.body,
                    timestamp: msg.timestamp * 1000
                }, {
                    timeout: 5000
                });
                console.log(`[✓] Mensagem enviada para webhook`);
            } catch (webhookError) {
                // Webhook não disponível ou erro - não é crítico
                console.log(`[!] Webhook não disponível (isso é normal se a IA não estiver configurada)`);
            }
        } catch (error) {
            console.error(`[!] Erro ao processar mensagem: ${error.message}`);
        }
    });

    client.initialize();
}

// Função para tentar reconectar automaticamente
function attemptReconnect() {
    if (isReconnecting) {
        return; // Já está tentando reconectar
    }
    
    if (reconnectAttempts >= maxReconnectAttempts) {
        const timestamp = new Date().toISOString();
        console.error(`\n[${timestamp}] ❌ Máximo de tentativas de reconexão atingido (${maxReconnectAttempts}).`);
        console.error(`[${timestamp}] ⚠️ Por favor, verifique manualmente ou reinicie o servidor.`);
        isReconnecting = false;
        return;
    }
    
    isReconnecting = true;
    reconnectAttempts++;
    const timestamp = new Date().toISOString();
    const delaySeconds = reconnectDelay / 1000;
    
    console.log(`\n[${timestamp}] 🔄 Tentativa de reconexão ${reconnectAttempts}/${maxReconnectAttempts} em ${delaySeconds} segundos...`);
    
    setTimeout(() => {
        if (!isReady) {
            console.log(`[${new Date().toISOString()}] 🔄 Reconectando...`);
            try {
                // Destroi cliente antigo se existir
                if (client) {
                    client.destroy().catch(() => {});
                }
                // Cria novo cliente
                initClient();
            } catch (error) {
                const timestamp = new Date().toISOString();
                console.error(`[${timestamp}] ❌ Erro ao tentar reconectar:`, error.message);
                isReconnecting = false;
                // Tenta novamente após delay
                setTimeout(() => {
                    isReconnecting = false;
                    attemptReconnect();
                }, reconnectDelay);
            }
        } else {
            isReconnecting = false;
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
        
        // Verifica se deveria estar conectado mas não está
        if (!isReady && !qrCodeData && !isReconnecting) {
            console.log(`\n[${timestamp}] ⚠️ Health Check: WhatsApp não está conectado. Tentando reconectar...`);
            attemptReconnect();
        } else if (isReady) {
            // Verifica se realmente está conectado (teste mais rigoroso)
            if (client && client.info) {
                // Está OK
            } else {
                console.log(`\n[${timestamp}] ⚠️ Health Check: Cliente marcado como pronto mas sem info. Reconectando...`);
                isReady = false;
                attemptReconnect();
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
    res.json({ status: 'ok', ready: isReady });
});

app.get('/qr', (req, res) => {
    // Verifica se foi solicitada uma porta específica
    const requestedPort = req.query.port ? parseInt(req.query.port) : port;
    
    // Se a porta solicitada é diferente da atual, retorna erro claro
    if (requestedPort != port) {
        return res.status(503).json({ 
            error: `Servidor na porta ${port} não pode atender porta ${requestedPort}.`,
            hint: `Cada porta precisa de um serviço Node.js separado no Railway. Crie um serviço com PORT=${requestedPort}`,
            currentPort: port,
            requestedPort: requestedPort
        });
    }
    
    // Usa a instância atual
    if (isReady) {
        return res.json({ ready: true, qr: null });
    }
    if (qrCodeData) {
        return res.json({ ready: false, qr: qrCodeData, hasQr: true });
    }
    return res.json({ ready: false, qr: null, hasQr: false });
});

app.post('/send', async (req, res) => {
    if (!isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        const { phone, message } = req.body;
        
        // Formata número
        let chatId = phone.replace(/\D/g, ''); // Remove caracteres não numéricos
        if (!chatId.includes('@c.us')) {
            chatId = chatId + '@c.us';
        }
        
        const result = await client.sendMessage(chatId, message);
        res.json({ success: true, messageId: result.id._serialized });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/status', (req, res) => {
    // Verifica se realmente está conectado tentando usar o cliente
    let actuallyReady = false;
    if (isReady && client) {
        try {
            // Verifica se o cliente está realmente conectado
            actuallyReady = client.info && client.info.wid;
        } catch (e) {
            actuallyReady = false;
        }
    }
    res.json({ 
        ready: actuallyReady || isReady, 
        hasQr: !!qrCodeData,
        actuallyConnected: actuallyReady,
        clientInitialized: !!client,
        reconnectInfo: {
            attempts: reconnectAttempts,
            maxAttempts: maxReconnectAttempts,
            isReconnecting: isReconnecting,
            autoReconnectEnabled: true
        }
    });
});

// Desconecta o WhatsApp
app.post('/disconnect', async (req, res) => {
    try {
        if (!client) {
            return res.status(400).json({ error: 'Cliente não inicializado' });
        }
        
        // Desconecta o cliente
        await client.logout();
        isReady = false;
        qrCodeData = null;
        
        console.log('✅ WhatsApp desconectado com sucesso');
        res.json({ success: true, message: 'WhatsApp desconectado com sucesso' });
    } catch (error) {
        console.error('❌ Erro ao desconectar:', error);
        // Mesmo com erro, marca como desconectado
        isReady = false;
        qrCodeData = null;
        res.json({ success: true, message: 'WhatsApp desconectado (pode ter havido um erro, mas foi desconectado)' });
    }
});

// Lista todas as conversas/chats do WhatsApp (melhorado)
app.get('/chats', async (req, res) => {
    if (!isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        // Busca TODOS os chats (sem limite)
        const chats = await client.getChats();
        
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
    if (!isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        const { chatId } = req.params;
        const limit = parseInt(req.query.limit) || 100; // Aumentado padrão para 100
        const beforeId = req.query.before; // Para paginação
        
        // Busca o chat pelo ID
        const chat = await client.getChatById(chatId);
        
        // Busca mensagens do chat com opção de paginação
        let fetchOptions = { limit: Math.min(limit, 1000) }; // Limite máximo de 1000
        if (beforeId) {
            try {
                const beforeMsg = await client.getMessageById(beforeId);
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

// Inicia servidor
app.listen(port, () => {
    const timestamp = new Date().toISOString();
    console.log(`\n[${timestamp}] 🚀 Servidor WhatsApp Web.js rodando em http://localhost:${port}`);
    console.log(`[${timestamp}] 📱 Client ID: ylada_bot_${port}`);
    console.log(`[${timestamp}] 📁 Sessão: .wwebjs_auth_${port}`);
    console.log(`[${timestamp}] 🔄 Auto-reconexão: ATIVADA (máx ${maxReconnectAttempts} tentativas)`);
    console.log(`[${timestamp}] 💚 Health Check: ATIVADO (verifica a cada 2 minutos)`);
    console.log(`[${timestamp}] Aguardando conexão...\n`);
    
    // Inicia cliente
    initClient();
    
    // Inicia health check
    startHealthCheck();
    
    // Cleanup ao encerrar
    process.on('SIGINT', () => {
        console.log('\n⚠️ Encerrando servidor...');
        if (healthCheckInterval) {
            clearInterval(healthCheckInterval);
        }
        if (client) {
            client.destroy();
        }
        process.exit(0);
    });
});

