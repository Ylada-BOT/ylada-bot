# 📦 Instalação - WhatsApp Web.js (Gratuito)

## 🎯 Esta solução permite:

✅ **100% GRATUITO**
✅ **Múltiplas instâncias** (vários números)
✅ **Funciona no seu computador**
✅ **Mais estável** que Selenium
✅ **Menor risco** de banimento

---

## 📋 Passo a Passo

### 1. Instalar Node.js

**macOS:**
```bash
# Via Homebrew
brew install node

# Ou baixe em: https://nodejs.org
```

**Verificar instalação:**
```bash
node --version
npm --version
```

### 2. Instalar Dependências

```bash
cd "/Users/air/EXTRATOR EUA"
npm install whatsapp-web.js qrcode-terminal express
```

### 3. Usar no Bot

O bot já está configurado para usar! Basta:

```bash
# Ativar modo webjs
export BOT_MODE=webjs

# Ou editar web/app.py e mudar para:
BOT_MODE = "webjs"
```

### 4. Iniciar

```bash
python web/app.py
```

Quando abrir, escaneie o QR Code que aparecer no terminal!

---

## 🔧 Múltiplas Instâncias

Para usar vários números:

```python
# Instância 1
handler1 = WhatsAppWebJSHandler(instance_name="numero1", port=3000)

# Instância 2  
handler2 = WhatsAppWebJSHandler(instance_name="numero2", port=3001)

# Instância 3
handler3 = WhatsAppWebJSHandler(instance_name="numero3", port=3002)
```

Cada uma terá seu próprio QR Code e sessão!

---

## ⚠️ Sobre Banimento

**Risco:** Médio (menor que Selenium, maior que Z-API)

**Dicas para evitar:**
- ✅ Não envie muitas mensagens de uma vez
- ✅ Use intervalos entre mensagens
- ✅ Não use para spam
- ✅ Use de forma natural

**Se for banido:**
- Geralmente é temporário (24-48h)
- Pode escanear QR Code novamente
- Considere Z-API para uso comercial

---

## 💡 Vantagens vs Z-API

| Característica | WhatsApp Web.js | Z-API |
|----------------|-----------------|-------|
| **Custo** | 🆓 Grátis | 💰 R$ 99,90/mês |
| **Múltiplas Instâncias** | ✅ Sim | ✅ Sim |
| **Risco de Ban** | ⚠️ Médio | ✅ Zero |
| **Estabilidade** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Suporte** | ❌ Não | ✅ Sim |

---

## 🚀 Pronto para usar!

Quer que eu ative isso agora no seu bot?

