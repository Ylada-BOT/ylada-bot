# Bot Ylada - Versão 100% GRATUITA 🆓

## ✅ Você NÃO precisa de API paga!

Este bot funciona **100% gratuito** de 3 formas:

### 1. 🟢 Modo SIMPLES (Recomendado para começar)
**Totalmente gratuito - funciona apenas na web**

- ✅ Não precisa de WhatsApp
- ✅ Não precisa de API
- ✅ Funciona direto no navegador
- ✅ Perfeito para testar e desenvolver

**Como usar:**
```python
from src.bot import LadaBot

bot = LadaBot(mode="simple")
# Pronto! Funciona na web
```

### 2. 🌐 Modo WhatsApp Web (Gratuito)
**Conecta direto no WhatsApp Web - sem API paga!**

- ✅ 100% gratuito
- ✅ Usa seu WhatsApp pessoal
- ✅ Funciona direto no navegador
- ⚠️ Precisa manter o navegador aberto

**Como usar:**
```bash
# 1. Instale Playwright
pip install playwright
playwright install chromium

# 2. Use o modo web
bot = LadaBot(mode="web")
bot.connect_whatsapp()  # Escaneia QR Code uma vez
```

### 3. 💰 Modo Z-API (Pago - opcional)
Só use se quiser recursos avançados. O modo SIMPLES já é suficiente!

---

## 🚀 Início Rápido (Modo Gratuito)

### Opção 1: Modo SIMPLES (Mais fácil)

```bash
cd "/Users/air/EXTRATOR EUA"
source .venv/bin/activate
python web/app.py
```

Acesse: http://localhost:5001

**Pronto!** O bot funciona na web. Você pode:
- Testar conversas
- Ver mensagens no dashboard
- Desenvolver sem custo

### Opção 2: WhatsApp Web (Gratuito)

```bash
# Instale Playwright
pip install playwright
playwright install chromium

# Edite web/app.py e mude para:
bot = LadaBot(mode="web")

# Execute
python web/app.py

# Quando abrir o navegador, escaneie o QR Code
# Depois, o bot funciona normalmente!
```

---

## 📊 Comparação dos Modos

| Recurso | SIMPLES | WhatsApp Web | Z-API |
|---------|---------|--------------|-------|
| **Custo** | 🆓 Grátis | 🆓 Grátis | 💰 Pago |
| **WhatsApp Real** | ❌ Não | ✅ Sim | ✅ Sim |
| **Precisa Navegador** | ❌ Não | ✅ Sim | ❌ Não |
| **Fácil de usar** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Recomendado para** | Testes/Dev | Uso pessoal | Produção |

---

## 💡 Qual Modo Usar?

### Use **SIMPLES** se:
- ✅ Quer testar sem custo
- ✅ Está desenvolvendo
- ✅ Não precisa WhatsApp real agora
- ✅ Quer ver como funciona

### Use **WhatsApp Web** se:
- ✅ Quer usar WhatsApp real
- ✅ Não quer pagar API
- ✅ Pode deixar navegador aberto
- ✅ É para uso pessoal/pequeno

### Use **Z-API** se:
- ✅ Precisa de escala
- ✅ Não pode manter navegador aberto
- ✅ Precisa de múltiplos números
- ✅ Tem orçamento

---

## 🎯 Recomendação

**Comece com o modo SIMPLES!**

1. Desenvolva e teste tudo
2. Quando estiver pronto, migre para WhatsApp Web
3. Só use Z-API se realmente precisar

**Tudo funciona 100% gratuito!** 🎉

