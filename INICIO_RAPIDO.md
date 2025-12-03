# 🚀 Início Rápido - Bot Ylada (Simplificado)

## ✅ Versão Simplificada - Apenas o Essencial

Esta versão tem **apenas o que você precisa usar agora**:
- ✅ Conversação básica
- ✅ Gerenciamento de contatos
- ✅ Envio de mensagens
- ✅ Dashboard web
- ✅ 100% gratuito (modo simples)

---

## 🎯 Como Usar (3 passos):

### 1. Iniciar o Bot
```bash
cd "/Users/air/EXTRATOR EUA"
source .venv/bin/activate
python web/app_simple.py
```

### 2. Acessar Dashboard
Abra no navegador: **http://localhost:5001**

### 3. Testar
- Envie mensagens de teste
- Veja contatos
- Use os fluxos de conversação

---

## 📱 Funcionalidades Disponíveis:

### Dashboard Web
- **http://localhost:5001/** - Painel principal
- Ver estatísticas
- Testar funcionalidades

### Enviar Mensagem
```bash
curl -X POST http://localhost:5001/send \
  -H "Content-Type: application/json" \
  -d '{"phone": "5511999999999", "message": "Olá!"}'
```

### Ver Contatos
```bash
curl http://localhost:5001/contacts
```

### Webhook (para receber mensagens)
```bash
curl -X POST http://localhost:5001/webhook \
  -H "Content-Type: application/json" \
  -d '{"phone": "5511999999999", "message": "oi"}'
```

---

## 🎯 O que está incluído:

✅ **Sistema de conversação** - Fluxos básicos configuráveis
✅ **Gerenciamento de contatos** - Histórico e tags
✅ **Dashboard web** - Interface visual
✅ **API REST** - Endpoints para integração
✅ **100% gratuito** - Modo simples (sem WhatsApp real)

---

## 💡 Quando precisar de WhatsApp real:

Se quiser conectar WhatsApp real depois, use:
- **Modo WebJS** (gratuito) - `python web/app.py` com `BOT_MODE=webjs`
- **Z-API** (pago) - Mais confiável para negócios

---

## 🎉 Pronto!

**Versão simplificada ativa!** Apenas o essencial para começar a usar agora.

