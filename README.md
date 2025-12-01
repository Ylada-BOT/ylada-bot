# 🤖 Ylada BOT - WhatsApp Automation Platform

Plataforma completa de automação para WhatsApp com gestão de contatos, campanhas, fluxos conversacionais e muito mais.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Funcionalidades

- 💬 **Chat ao Vivo**: Interface completa para gerenciar conversas do WhatsApp
- 👥 **Gestão de Audiência**: Contatos, tags, filtros e segmentação
- 📢 **Campanhas**: Criação de campanhas com QR codes e links personalizados
- 📡 **Transmissões**: Envio em massa com atraso inteligente
- 🎨 **Construtor de Fluxos**: Editor visual drag-and-drop para criar fluxos conversacionais
- ⚙️ **Automação**: Palavras-chave, sequências e webhooks
- 📊 **Dashboard**: Estatísticas e métricas em tempo real
- 🔐 **Multi-usuário**: Sistema de usuários e permissões

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Node.js 18+ (para WhatsApp Web.js)
- Conta Supabase (banco de dados)
- Conta Vercel (deploy)

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/Ylada-BOT/ylada-bot.git
cd ylada-bot

# Instale dependências Python
pip install -r requirements.txt

# Instale dependências Node.js
npm install

# Configure variáveis de ambiente
cp ENV_EXAMPLE.txt .env
# Edite .env com suas credenciais

# Inicie o servidor Flask
python web/app.py

# Em outro terminal, inicie o servidor WhatsApp (opcional)
node whatsapp_server.js
```

Acesse: http://localhost:5002

## 📦 Deploy

### Deploy na Vercel

1. **Configure Supabase**
   - Crie um projeto no [Supabase](https://app.supabase.com)
   - Execute o SQL do arquivo `DEPLOY.md` (seção 1.2)
   - Copie URL e API Keys

2. **Configure Vercel**
   - Importe este repositório no [Vercel](https://vercel.com)
   - Adicione variáveis de ambiente:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `SUPABASE_SERVICE_KEY`
     - `SECRET_KEY`
     - `BOT_MODE=webjs`

3. **Deploy**
   - Clique em "Deploy"
   - Aguarde o processo concluir

📖 **Guia completo**: Veja `DEPLOY.md` ou `QUICK_DEPLOY.md`

## 🏗️ Estrutura do Projeto

```
ylada-bot/
├── web/                 # Aplicação Flask
│   ├── app.py          # Servidor principal
│   └── templates/      # Templates HTML
├── src/                # Código fonte
│   ├── bot_simple.py   # Bot simplificado
│   ├── whatsapp_webjs_handler.py  # Handler WhatsApp
│   └── supabase_client.py  # Cliente Supabase
├── config/             # Configurações
│   └── config.yaml     # Config do bot
├── api/                # Entry point Vercel
├── whatsapp_server.js  # Servidor Node.js WhatsApp
└── requirements.txt    # Dependências Python
```

## 🛠️ Tecnologias

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Banco de Dados**: Supabase (PostgreSQL)
- **WhatsApp**: WhatsApp Web.js
- **Deploy**: Vercel
- **Infraestrutura**: Serverless Functions

## 📚 Documentação

- `DEPLOY.md` - Guia completo de deploy
- `QUICK_DEPLOY.md` - Deploy rápido (5 minutos)
- `DEPLOY_CHECKLIST.md` - Checklist de deploy
- `DESIGN_BOTCONVERSA_COMPLETO.md` - Documentação de design

## 🔧 Configuração

### Modos de Operação

- **webjs**: WhatsApp Web.js (gratuito, recomendado)
- **zapi**: Z-API (pago, mais estável)
- **simple**: Modo simulação (desenvolvimento)

Configure em `.env`:
```env
BOT_MODE=webjs
```

## 📱 Conectar WhatsApp

1. Acesse `/qr` no dashboard
2. Escaneie o QR Code com seu WhatsApp
3. Aguarde a conexão ser estabelecida
4. Pronto! Suas conversas aparecerão no chat

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

**Ylada BOT Team**

- GitHub: [@Ylada-BOT](https://github.com/Ylada-BOT)

## 🙏 Agradecimentos

- [WhatsApp Web.js](https://github.com/pedroslopez/whatsapp-web.js)
- [Flask](https://flask.palletsprojects.com/)
- [Supabase](https://supabase.com/)
- [Vercel](https://vercel.com/)

## 📞 Suporte

Para suporte, abra uma [issue](https://github.com/Ylada-BOT/ylada-bot/issues) no GitHub.

---

⭐ Se este projeto foi útil, considere dar uma estrela!
