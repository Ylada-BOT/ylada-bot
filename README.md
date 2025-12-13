# BOT by YLADA

**Integração WhatsApp + Inteligência Artificial**

Solução simples para automatizar respostas do WhatsApp usando IA.

## 🚀 Início Rápido

```bash
# Instalar dependências
npm install
pip install -r requirements.txt

# Iniciar
python web/app_simple.py
```

Acesse: http://localhost:5002

## ✨ Funcionalidades

- ✅ Conectar WhatsApp via QR Code
- ✅ Configurar IA (OpenAI ou Anthropic)
- ✅ Respostas automáticas com IA
- ✅ Dashboard simples

## 📁 Estrutura

```
BOT by YLADA/
├── web/
│   ├── app_simple.py          # Servidor Flask
│   ├── templates/
│   │   ├── dashboard_simple.html
│   │   └── qr_simple.html
│   └── static/assets/logo.png
├── src/
│   ├── whatsapp_webjs_handler.py
│   └── ai_handler.py
├── whatsapp_server.js
└── requirements.txt
```

## 🔧 Configuração

1. Conecte WhatsApp (QR Code)
2. Configure IA (API Key)
3. Pronto! Respostas automáticas

---

**Simples. Limpo. Focado.**
