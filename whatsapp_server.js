const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
const port = 5001;

app.use(express.json());

let client = null;
let qrCodeData = null;
let isReady = false;

// Inicializa cliente
function initClient() {
    client = new Client({
        authStrategy: new LocalAuth({
            clientId: 'ylada_bot'
        }),
        puppeteer: {
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
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
    });

    client.on('ready', () => {
        console.log('\n✅ WhatsApp conectado com sucesso!');
        isReady = true;
        qrCodeData = null;
    });

    client.on('authenticated', () => {
        console.log('✅ Autenticado!');
    });

    client.on('auth_failure', (msg) => {
        console.error('❌ Falha na autenticação:', msg);
        isReady = false;
    });

    client.on('disconnected', (reason) => {
        console.log('⚠️ Desconectado:', reason);
        isReady = false;
    });

    client.initialize();
}

// Rotas da API
app.get('/health', (req, res) => {
    res.json({ status: 'ok', ready: isReady });
});

app.get('/qr', (req, res) => {
    res.json({ qr: qrCodeData, ready: isReady });
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
    res.json({ ready: isReady, hasQr: !!qrCodeData });
});

// Lista todas as conversas/chats do WhatsApp
app.get('/chats', async (req, res) => {
    if (!isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        const chats = await client.getChats();
        
        // Formata os chats para retornar apenas o necessário
        const formattedChats = chats.map(chat => {
            const contact = chat.contact || {};
            const lastMessage = chat.lastMessage || {};
            
            return {
                id: chat.id._serialized,
                name: contact.pushname || contact.name || chat.name || 'Sem nome',
                phone: chat.id.user || '',
                isGroup: chat.isGroup,
                unreadCount: chat.unreadCount || 0,
                lastMessage: lastMessage.body || '',
                timestamp: lastMessage.timestamp ? lastMessage.timestamp * 1000 : Date.now(),
                pinned: chat.pinned || false
            };
        });
        
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

// Busca mensagens de um chat específico
app.get('/chats/:chatId/messages', async (req, res) => {
    if (!isReady) {
        return res.status(400).json({ error: 'Cliente não conectado. Escaneie o QR Code primeiro.' });
    }
    
    try {
        const { chatId } = req.params;
        const limit = parseInt(req.query.limit) || 50;
        
        // Busca o chat pelo ID
        const chat = await client.getChatById(chatId);
        
        // Busca mensagens do chat
        const messages = await chat.fetchMessages({ limit: limit });
        
        // Formata as mensagens
        const formattedMessages = messages.map(msg => {
            return {
                id: msg.id._serialized,
                body: msg.body || '',
                from: msg.from || chatId,
                fromMe: msg.fromMe,
                timestamp: msg.timestamp * 1000,
                type: msg.type,
                hasMedia: msg.hasMedia,
                mediaUrl: msg.hasMedia ? (msg.mediaUrl || '') : null
            };
        });
        
        // Ordena por timestamp (mais antiga primeiro)
        formattedMessages.sort((a, b) => a.timestamp - b.timestamp);
        
        res.json({
            success: true,
            messages: formattedMessages,
            total: formattedMessages.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Inicia servidor
app.listen(port, () => {
    console.log(`\n🚀 Servidor WhatsApp Web.js rodando em http://localhost:${port}`);
    console.log('Aguardando conexão...\n');
    initClient();
});

