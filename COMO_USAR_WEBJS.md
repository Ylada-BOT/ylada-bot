# 🚀 Como Usar WhatsApp Web.js (Gratuito)

## ✅ Tudo instalado e pronto!

### Status:
- ✅ Node.js instalado (v22.18.0)
- ✅ Dependências instaladas
- ✅ Servidor Node.js rodando na porta 3000
- ✅ Bot Flask rodando na porta 5001
- ✅ Modo WebJS ativado

---

## 📱 Próximos Passos:

### 1. Ver QR Code

**Opção A: No Terminal**
- Olhe o terminal onde o bot está rodando
- Você verá um QR Code em ASCII
- Escaneie com seu WhatsApp

**Opção B: Na Web**
- Acesse: http://localhost:5001/qr
- Veja o QR Code visual
- Escaneie com seu WhatsApp

### 2. Escanear QR Code

1. Abra WhatsApp no celular
2. Vá em: **Configurações** > **Aparelhos conectados**
3. Toque em: **Conectar um aparelho**
4. Escaneie o QR Code

### 3. Pronto!

Depois de escanear, o bot estará conectado e funcionando!

---

## 🎯 Como Testar:

### Enviar Mensagem:
```bash
curl -X POST http://localhost:5001/send \
  -H "Content-Type: application/json" \
  -d '{"phone": "5511999999999", "message": "Teste!"}'
```

### Ver Status:
```bash
curl http://localhost:3000/status
```

---

## 🔧 Múltiplas Instâncias:

Para usar vários números, edite `src/bot.py`:

```python
# Instância 1 (porta 3000)
handler1 = WhatsAppWebJSHandler("numero1", port=3000)

# Instância 2 (porta 3001)  
handler2 = WhatsAppWebJSHandler("numero2", port=3001)
```

Cada uma terá seu próprio QR Code!

---

## ⚠️ Importante:

- **Mantenha o terminal aberto** (servidor precisa estar rodando)
- **Primeira vez:** Escaneie QR Code
- **Próximas vezes:** Sessão fica salva (não precisa escanear)
- **Se desconectar:** Escaneie QR Code novamente

---

## 🎉 Pronto para usar!

Acesse: **http://localhost:5001/qr** para ver o QR Code!

