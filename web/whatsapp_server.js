
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
const port = 5001;

app.use(express.json());

let client = null;
let qrCodeData = null;
let isReady = false;

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
        console.log('\nEscaneie o QR Code acima com seu WhatsApp\n');
    });

    client.on('ready', () => {
        console.log('\n✅ WhatsApp conectado!');
        isReady = true;
        qrCodeData = null;
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

app.get('/health', (req, res) => {
    res.json({ status: 'ok', ready: isReady });
});

app.get('/qr', (req, res) => {
    res.json({ qr: qrCodeData, ready: isReady });
});

app.post('/send', async (req, res) => {
    if (!isReady) {
        return res.status(400).json({ error: 'Cliente não conectado' });
    }
    try {
        const { phone, message } = req.body;
        let chatId = phone.replace(/\D/g, '');
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
            // Tenta verificar se o cliente está realmente conectado
            actuallyReady = client.info && client.info.wid;
        } catch (e) {
            actuallyReady = false;
        }
    }
    res.json({ ready: actuallyReady || isReady, hasQr: !!qrCodeData, actuallyConnected: actuallyReady });
});

// Lista todas as conversas/chats do WhatsApp
app.get('/chats', async (req, res) => {
    if (!isReady || !client) {
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

app.listen(port, () => {
    console.log(`\n🚀 Servidor rodando em http://localhost:${port}\n`);
    initClient();
});
